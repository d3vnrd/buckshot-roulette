from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version
from typing import override
from abc import abstractmethod

from textual import on, work
from textual.binding import Binding
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.app import ComposeResult, App
from textual.widget import Widget
from textual.widgets import (
    Footer,
    Input,
    Label,
    ProgressBar,
    RichLog,
)

from buckshot import BuckshotEngine

# ---Create Textual Observers from Buckshot Observers---
class TextualObserver(Widget, BuckshotEngine.BuckshotObserver):
    def __init__(self, engine: BuckshotEngine) -> None:
        Widget.__init__(self)
        engine.attach(self)

# ---Widgets to report Board current state---
class BoardLogs(TextualObserver):
    message: reactive[str] = reactive("")

    def compose(self) -> ComposeResult:
        yield RichLog(id="game-logs")

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState):
        self.message = state.message

    def watch_message(self, old:str , new: str):
        if new and new != old:
            self.query_one("#game-logs", RichLog).write(new)

class BoardPlayersInfo(TextualObserver):
    player1_name: reactive[str] = reactive("Player 1")
    player1_health: reactive[int] = reactive(0)
    player1_total_items: reactive[int] = reactive(0)
    
    player2_name: reactive[str] = reactive("Player 2")
    player2_health: reactive[int] = reactive(0)
    player2_total_items: reactive[int] = reactive(0)

    @override
    def compose(self) -> ComposeResult:
        with Vertical():
            for player in ["player1", "player2"]:
                with Horizontal():
                    yield Label("?", id=f"{player}-name")
                    
                    with HorizontalGroup():
                        yield Label("Health: ")
                        yield ProgressBar(
                            total=0,
                            show_percentage=False,
                            show_eta=False,
                            classes="full-width",
                            id=f"{player}-health"
                        )
                        yield Label(" 0/0")
                    
                    with HorizontalGroup():
                        yield Label("Total Items: ")
                        yield Label("?", classes="right-align", id=f"{player}-total-items")

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState):
        """Update reactive attributes"""
        self.player1_name = state.players[0].name
        self.player1_health = state.players[0].health
        self.player1_total_items = state.players[0].total_items
        
        self.player2_name = state.players[1].name
        self.player2_health = state.players[1].health
        self.player2_total_items = state.players[1].total_items

    def on_mount(self):
        watchers: dict[str, tuple] = {
            "name": (Label, lambda u, v: u.update(v)),
            "health": (ProgressBar, lambda u, v: u.update(progress=v)),
            "total_items": (Label, lambda u, v: u.update(str(v)))
        }

        def make_watcher(query, widget_cls, handler):
            def watch_fn(v):
                widget = self.query_one(query, widget_cls)
                handler(widget, v)
            return watch_fn

        for pid in ["player1", "player2"]:
            for attr, (widget, handler) in watchers.items():
                query = f"#{pid}-{attr.replace("_", "-")}"
                attr_name = f"{pid}_{attr}"

                self.watch(
                    self,
                    attr_name,
                    make_watcher(query, widget, handler)
                )

# ---Prompts (modal-screens) to handle user interactions---
class SetupPrompt(ModalScreen[tuple]):
    DEFAULT_CLASSES = "footer-prompt"

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

        p01name = self.query_one("#input01", Input).value
        p02name = self.query_one("#input02", Input).value
        self.dismiss((p01name, p02name))

class ActionsPrompt(ModalScreen[list[str]]):
    DEFAULT_CLASSES = "footer-prompt"
    BINDINGS = [
        ("5", "use_handcuff", "Use Handcuff"),
        ("4", "use_cigarette", "Use Cigarette"),
        ("3", "use_handsaw", "Use Handsaw"),
        ("2", "use_beer", "Use Beer"),
        ("1", "use_magnifier", "Use Manifying Glass"),
        ("space", "shoot", "Shoot"),
        ("q", "dismiss", "Exit"),
    ]

    class TargetPrompt(ModalScreen[bool]):
        DEFAULT_CLASSES = "footer-prompt"
        BINDINGS = [
            ("1", "dismiss(True)", "Opponent"),
            ("0", "dismiss(False)", "Self"),
        ]

        def compose(self) -> ComposeResult:
            yield Footer()

    def __init__(self, state: BuckshotEngine.BuckshotState) -> None:
        super().__init__()
        self.state = state

    def compose(self) -> ComposeResult:
        yield Footer()

    @work
    async def action_shoot(self):
        self.dismiss([
            "shoot",
            "target" 
            if await self.app.push_screen_wait(self.TargetPrompt()) 
            else "self"
        ])

    def action_use_magnifier(self):
        self.dismiss(['magnifier'])

    def action_use_beer(self):
        self.dismiss(['beer'])

    def action_use_handsaw(self):
        self.dismiss(['handsaw'])

    def action_use_cigarette(self):
        self.dismiss(['cigarette'])

    def action_use_handcuff(self):
        self.dismiss(['handcuff'])

    @override
    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        p_inv = self.state.players[self.state.curr_turn_idx].inv_status

        for item in ["magnifier", "beer", "handsaw", "cigarette", "handcuff"]:
            if action == f"use_{item}" and p_inv.get(item, 0) <= 0:
                return None

        return True

# ---Screen used in App---
class BaseScreen(Screen):
    BINDINGS = [("q", "dismiss")]

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Label(f"[dim]{self.app.title} - {self.app.sub_title}[/dim]")
            yield Label("[dim]13:10:58[/dim]", classes="right-align")

        with Container(id='main-contents'):
            yield from self.assign()

        yield Footer()

    def key_q(self):
        self.dismiss()

    @abstractmethod
    def assign(self) -> ComposeResult: 
        pass

class DefaultScreen(BaseScreen):
    BINDINGS = [
        Binding("q", "app.quit", priority=True),
        ("h", "app.push_screen('help')", "Help"),
        ("c", "app.push_screen('credit')", "Credit"),
        ("space", "app.push_screen('game')", "Start"),
    ]

    @override
    def assign(self):
        with Vertical():
            yield Label("[bold orange]BUCKSHOTxROULETTE[/bold orange]", id="title")
            yield Label(f"[dim]x{'-'*45}x[/dim]", id="divider")
            yield Label("[dim]Based on Buckshot Roulette by Mike Klubnika[/dim]", classes="other")
            yield Label("[dim]Press <Space> to continue[/dim]", classes="other")

class HelpScreen(BaseScreen):
    @override
    def assign(self) -> ComposeResult:
        yield Label("This is the help screen")

class CreditScreen(BaseScreen):
    @override
    def assign(self) -> ComposeResult:
        yield Label("This is the credit screen")

class BoardScreen(BaseScreen):
    _engine = BuckshotEngine()

    BINDINGS = [
        ("h", "app.push_screen('help')", "Help"),
        ("space", "parse_actions", "Act"),
    ]

    @override
    def assign(self) -> ComposeResult:
        yield BoardLogs(self._engine)
        yield BoardPlayersInfo(self._engine)

    @work
    async def on_mount(self):
        self._engine.setup(*await self.app.push_screen_wait(SetupPrompt()))

    @work
    async def action_parse_actions(self):
        inputs = await self.app.push_screen_wait(ActionsPrompt(self._engine.state))
        if not inputs: 
            return

        self._engine.execute(inputs)

# ---Main Application---
class TextualBuckshot(App): 
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = "style.tcss" 
    SCREENS = {
        "default": DefaultScreen,
        "credit": CreditScreen,
        "help": HelpScreen,
        "game": BoardScreen,
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
