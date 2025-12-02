from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version
from typing import override
from abc import abstractmethod

from textual import on, work
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.app import ComposeResult, App
from textual.widgets import (
    Input,
    Label,
    ProgressBar,
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

        with Container(id="contents"):
            yield from self.assign()

    def key_escape(self):
        self.dismiss()

    @abstractmethod
    def assign(self) -> ComposeResult: 
        pass

class DefaultScreen(BaseScreen):
    BINDINGS = [
        ("h", "app.push_screen('help')", "Help"),
        ("c", "app.push_screen('credit')", "Credit"),
        ("space", "app.push_screen('game')", "Start"),
    ]

    @override
    def key_escape(self):
        self.app.exit()

    @override
    def assign(self):
        yield Static("[bold orange]BUCKSHOTxROULETTE[/bold orange]", id="title")
        yield Static(f"[dim]x{'-'*45}x[/dim]", id="divider")
        yield Static("[dim]Based on Buckshot Roulette by Mike Klubnika[/dim]", classes="other")
        yield Static("[dim]<space> Starts[/dim]", classes="other")
        yield Static("[dim]<h> Help[/dim]", classes="other")
        yield Static("[dim]<c> Credit[/dim]", classes="other")
        yield Static("[dim]<escape> Exit[/dim]", classes="other")

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
        ("space", "parse_item('gun')"),
        *[(str(i), f"parse_item('{name}')") for i, name in enumerate(
            ["magnifier", "beer", "handsaw", "cigarette", "handcuff"],
            start=1
        )]
    ]

    # ---Extra prompts to handle player interactions and dynamic bindings---
    class SetupPrompt(ModalScreen[tuple]):
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

    class TargetPrompt(ModalScreen[str|None]):
        DEFAULT_CLASSES = "hidden-prompt"
        BINDINGS = [
            ("1", "dismiss('self')"),
            ("2", "dismiss('opponent')"),
            ("escape", "dismiss")
        ]

    # ---Screen widgets---
    class Logs(RichLog, BuckshotEngine.BuckshotObserver):
        message: reactive[str] = reactive("")

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(id="game-logs")
            engine.attach(self)

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            self.message = state.message

        def watch_message(self, old: str , new: str):
            if new and new != old:
                self.write(new)

    class PlayerInfo(Horizontal, BuckshotEngine.BuckshotObserver):
        _pname = reactive("Player")
        _health = reactive(0)
        _health_cap = reactive(0)
        _total_items = reactive(0)

        def __init__(self, engine: BuckshotEngine, idx: int) -> None:
            super().__init__()
            engine.attach(self)
            self.idx = idx

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState) -> None:
            player = state.players[self.idx]
            self._pname = player.name
            self._health = player.health
            self._total_items = player.total_items
            self._health_cap = state.stage.health_cap

        @override
        def compose(self) -> ComposeResult:
            yield Label("?", id=f"player{self.idx}-name")

            with HorizontalGroup(id=f"player{self.idx}-health"):
                yield ProgressBar(
                    total=0,
                    show_percentage=False,
                    show_eta=False,
                    id=f"player{self.idx}-health-bar"
                )
                yield Static(" ")
                yield Label("?", id=f"player{self.idx}-health-indicator")

            yield Label("Total items: ?", id=f"player{self.idx}-total-items")

        def on_mount(self):
           watchers: dict[str, tuple] = {
                "_pname": (f"#player{self.idx}-name", Label, lambda t, v: t.update(v + ": ")),
                "_health": (f"#player{self.idx}-health-bar", ProgressBar, lambda t, v: t.update(progress=v)),
                "_total_items": (f"#player{self.idx}-total-items", Label, lambda t, v: t.update(f"Total items: {v}")),
                "_health_cap": (f"#player{self.idx}-health-bar", ProgressBar, lambda t, v: t.update(total=v))
            }
    
           def make_watcher(query, widget, handler):
                def watch_fn(v):
                    target = self.query_one(query, widget)
                    handler(target, v)
                return watch_fn
    
           for attr, (query, widget, handler) in watchers.items():
               self.watch(
                   self,
                   attr,
                   make_watcher(query, widget, handler)
               )

    # ---Class business logic---
    @override
    def assign(self) -> ComposeResult:
        yield self.Logs(self._engine)
        with Vertical():
            yield self.PlayerInfo(self._engine, 0)
            yield self.PlayerInfo(self._engine, 1)

    def write(self, mess: str):
        self.query_one(self.Logs).message = mess

    @work
    async def on_mount(self):
        self._engine.setup(*await self.app.push_screen_wait(self.SetupPrompt()))

    @work
    async def action_parse_item(self, item: str):
        if item not in ["magnifier", "beer", "handsaw", "cigarette", "handcuff", "gun"]:
            return

        actions = [item]
        if item == "gun":
            self.write("Choose a target: <1> self | <2> opponent")
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
