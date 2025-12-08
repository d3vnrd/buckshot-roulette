from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version
from typing import override


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
    def key_escape(self) -> None:
        self.dismiss()

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
    def compose(self):
        yield Static(f"[bold orange]{self.app.title}[/bold orange]", id="title")
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
    def compose(self) -> ComposeResult:
        yield Label("This is the help screen")

class CreditScreen(BaseScreen):
    @override
    def compose(self) -> ComposeResult:
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
        _stage = {1: "I", 2: "II", 3: "III"}

        class StatLabel(Static):
            def __init__(self, content: str) -> None:
                super().__init__(content)
                self.styles.height = 1

        class StatValue(Static):
            def __init__(self, content: str, id: str) -> None:
                super().__init__(content, id=id)
                self.styles.text_align = "right"
                self.styles.height = 1

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__()
            engine.attach(self)

        def compose(self) -> ComposeResult:
            with Container(id="game-status-content"):
                yield self.StatLabel("Bullets Left:")
                yield self.StatValue("?", id="game-status-chamber")
                yield self.StatLabel("Current Turn:")
                yield self.StatValue("?", id="game-status-turn")
                yield self.StatLabel("Items per reload:")
                yield self.StatValue("?", id="game-status-items-add")
                yield self.StatLabel("Stage:")
                yield self.StatValue("?", id="game-status-stage")

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            self.query_one("#game-status-chamber", Static).update("  ".join(["󰲅" * state.shotgun.bullets_left]))
            self.query_one("#game-status-turn", Static).update(state.players[state.turn].name)
            self.query_one("#game-status-items-add", Static).update(str(state.items_per_reload))
            self.query_one("#game-status-stage", Static).update(self._stage.get(state.stage, "???"))

    class PlayersInfo(Container, BuckshotEngine.BuckshotObserver):
        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__()
            engine.attach(self)
            self.border_title = "Hey, ya good? Whacha got?"

        def compose(self) -> ComposeResult:
            yield Static("Just a simple player containers")

    # ---Class business logic---
    def __init__(self, p1_name: str, p2_name: str) -> None:
        super().__init__()
        self._engine = BuckshotEngine(p1_name, p2_name)
        self.border_title = f"󰍉 󱄾 {self.app.title} 󱆉 󰹈"
        self.border_subtitle = self.app.sub_title

    @override
    def compose(self) -> ComposeResult:
        with ScrollableContainer(id="board-status"):
            yield self.GameStatus(self._engine)
            with Horizontal(id="bot-panel"):
                yield self.GameLogs(self._engine)
                yield self.PlayersInfo(self._engine)

    def write(self, mess: str):
        self.query_one(self.GameLogs).message = mess

    @override
    def key_escape(self) -> None:
        self.action_confirm_exit()

    def on_mount(self):
        self._engine.reset()

    def on_resize(self):
        width, height = self.app.size
        main_content = self.query_one("#board-status", ScrollableContainer)

        if width/height < 3.0:
            main_content.styles.width = "1fr"
            return

        main_content.styles.width = "60%"

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
        self.app.title = "BUCKSHOTxROULETTE"
        self.app.sub_title = f"v{self.get_version()}"

    def on_mount(self):
        self.push_screen("default")

    def get_version(self):
        try:
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"
