from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version
from typing import override
from abc import abstractmethod


from textual import on, work
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.app import ComposeResult, App
from textual.widgets import (
    Input,
    Label,
    RichLog,
    Static,
)

from buckshot import BuckshotEngine

# ---Screen used in App---
class BaseScreen(Screen):
    DEFAULT_CLASSES = "screen-padding"

    def compose(self) -> ComposeResult:
        with Horizontal(id="header"):
            yield Label(f"[dim]{self.app.title} - {self.app.sub_title}[/dim]")
            yield Label("[dim]13:10:58[/dim]", classes="right-align")

        with ScrollableContainer(id="contents"):
            yield from self.assign()

    def key_escape(self) -> None:
        self.dismiss()

    @abstractmethod
    def assign(self) -> ComposeResult: 
        pass

class DefaultScreen(BaseScreen):
    BINDINGS = [
        ("h", "app.push_screen('help')", "Help"),
        ("c", "app.push_screen('credit')", "Credit"),
        ("space", "load_game", "Start"),
    ]

    class SetupPrompt(ModalScreen[tuple[str, str]]):
        def compose(self) -> ComposeResult:
            yield Label("Enter player's names:")
            yield Input(compact=True, max_length=8, id="input01")
            yield Input(compact=True, max_length=8, id="input02")

        @on(Input.Submitted, "#input01")
        def next(self):
            self.set_focus(self.query_one("#input02"))

        @on(Input.Submitted, "#input02")
        def confirm_setup(self):
            if not self.query_one("#input01", Input).value:
                self.set_focus(self.query_one("#input01"))
                return

            self.dismiss((
                self.query_one("#input01", Input).value,
                self.query_one("#input02", Input).value
            ))

    @override
    def key_escape(self):
        self.app.exit()

    @override
    def assign(self):
        yield Static("[bold orange]BUCKSHOTxROULETTE[/bold orange]", id="title")
        yield Static(f"[dim]x{'-'*45}x[/dim]", id="divider")
        yield Static("[dim]Based on Buckshot Roulette by Mike Klubnika[/dim]")
        yield Static("[dim]<space> Starts[/dim]")
        yield Static("[dim]<h> Help[/dim]")
        yield Static("[dim]<c> Credit[/dim]")
        yield Static("[dim]<escape> Exit[/dim]")

    @work
    async def action_load_game(self):
        players = await self.app.push_screen_wait(self.SetupPrompt())
        self.app.push_screen(BoardScreen(*players))

class HelpScreen(BaseScreen):
    @override
    def assign(self) -> ComposeResult:
        yield Label("This is the help screen")

class CreditScreen(BaseScreen):
    @override
    def assign(self) -> ComposeResult:
        yield Label("This is the credit screen")

class BoardScreen(BaseScreen):
    BINDINGS = [
        ("space", "parse_item('gun')"),
        *[(str(i), f"parse_item('{name}')") for i, name in enumerate(
            ["magnifier", "beer", "handsaw", "cigarette", "handcuff"],
            start=1
        )],
    ]

    # ---Extra prompts to handle player interactions and dynamic bindings---
    class TargetPrompt(ModalScreen[str|None]):
        DEFAULT_CLASSES = "hidden-prompt"
        BINDINGS = [
            ("1", "dismiss('self')"),
            ("2", "dismiss('opponent')"),
            ("escape", "dismiss")
        ]

    class ConfirmExit(ModalScreen[bool]):
        BINDINGS = [
            ("y", "dismiss(True)"),
            ("n", "dismiss(False)")
        ]

        def compose(self) -> ComposeResult:
            yield Static("You scare? Y|N")

    # ---Screen widgets---
    class GameLogs(RichLog, BuckshotEngine.BuckshotObserver):
        message: reactive[str] = reactive("")

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__()
            engine.attach(self)

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            self.message = state.message

        def watch_message(self, old: str , new: str):
            if new and new != old:
                self.write(new)

    class GameStatus(Container, BuckshotEngine.BuckshotObserver):

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__()
            engine.attach(self)

        @property
        def title(self, title: str = "BUCKSHOTxROULETTE", fill_char:str = "-"):
            container_width = self.size.width
            
            available_width = container_width - len(title) - 4  # -4 for "x x" and spaces
            
            if available_width > 0:
                fill_left = available_width // 2
                fill_right = available_width - fill_left  # Handle odd widths
                
                centered = f"x{fill_char * fill_left} {title} {fill_char * fill_right}x"
            else:
                centered = f"x {title} x"
            
            return centered

        def compose(self) -> ComposeResult:
            yield Static(self.title)

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            pass

        def on_resize(self):
            self.query_one(Static).update(self.title)

    # ---Class business logic---
    def __init__(self, p1_name: str, p2_name: str) -> None:
        super().__init__()
        self._engine = BuckshotEngine(p1_name, p2_name)

    @override
    def assign(self) -> ComposeResult:
        yield self.GameStatus(self._engine)
        # yield self.GameLogs(self._engine)

    def write(self, mess: str):
        self.query_one(self.GameLogs).message = mess

    @override
    def key_escape(self) -> None:
        self.action_confirm_exit()

    def on_mount(self):
        self._engine.reset()

    def on_resize(self):
        width, height = self.app.size
        # logs = self.query_one(self.GameLogs)
        stats = self.query_one(self.GameStatus)

        if width/height < 3.0:
            # logs.styles.width = "1fr"
            stats.styles.width = "1fr"
            return

        # logs.styles.width = "60%"
        stats.styles.width = "60%"

    @work
    async def action_confirm_exit(self):
        if await self.app.push_screen_wait(self.ConfirmExit()):
            self.dismiss()

    @work
    async def action_parse_item(self, item: str):
        if item not in self._engine._valid_actions:
            return

        actions = [item]
        if item == "gun":
            self.write(" | ".join(["󱆉", "󱄾", "󰍉", "󱄖", "󰹈"]))
            target = await self.app.push_screen_wait(self.TargetPrompt())

            if target is None:
                self.write("Action Canceled")
                return

            actions.append(target)

        self._engine.execute(actions)

# ---Main Application---
class TextualBuckshot(App): 
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "style.tcss" 
    SCREENS = {
        "default": DefaultScreen,
        "credit": CreditScreen,
        "help": HelpScreen,
    }

    def __init__(self, args: list[str] | None = None):
        super().__init__()
        self.app.title = "buckshot-roulette"
        self.app.sub_title = f"v{self.get_version()}"

    def on_mount(self):
        self.push_screen("default")

    def get_version(self):
        try:
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"
