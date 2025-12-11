from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar, override
from importlib.metadata import PackageNotFoundError, version

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, HorizontalGroup, ScrollableContainer
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import ModalScreen, Screen
from textual.widget import Widget
from textual.widgets import (
    Footer,
    Input,
    Label,
    RichLog,
    Static
)

from buckshot.engine import BuckshotEngine
from buckshot.entity import Player

class _View(Screen):
    DEFAULT_CSS = """
    _View ScrollableContainer {
        overflow: auto auto;
        align: center middle;
        scrollbar-background: $background;
        scrollbar-background-active: $background;
        scrollbar-background-hover: $background;
        scrollbar-corner-color: $background;
        scrollbar-color: $background;
        scrollbar-color-active: white;
        scrollbar-color-hover: white;
        scrollbar-size: 1 1;
    }

    _View Static {
        width: 1fr;
        height: 1;
    }

    _View .center-align {
        content-align: center middle;
    }

    _View .right-align {
        content-align: right middle;
    }
    """

    PREV_VIEW: str = 'title'
    NAME: str

    class ContentWrapper(Container):
        DEFAULT_CSS = """
        ContentWrapper {
            width: 80;
            height: 40;
            border: round white;
            border-title-align: center;
            border-subtitle-align: right;
            align: center middle;
        }
        """

        def __init__(self, *children: Widget) -> None:
            super().__init__(*children)
            self.border_title = f"󰍉 󱄾 {self.app.title} 󱆉 󰹈"
            self.border_subtitle = f"v{self.app.sub_title}"

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(self.ContentWrapper(*self.assign()))

    def key_q(self) -> None:
        self.app.switch_mode(self.PREV_VIEW)

    @abstractmethod
    def assign(self) -> ComposeResult:
        pass

T = TypeVar("T")
class _Prompt(ModalScreen[T]):
    DEFAULT_CSS = """
    _Prompt {
        background: rgba(0, 0, 0, 0)
    }
    """

    def compose(self) -> ComposeResult:
        yield Footer()

    def key_q(self):
        self.dismiss()

# ---Views used by App---
class TitleView(_View):
    NAME = 'title'
    BINDINGS = [('space', "app.switch_mode('board')")]

    def assign(self) -> ComposeResult:
        yield from (Label(l, classes="center-align") for l in [
            f"[bold orange]{self.app.title}[/bold orange]",
            f"[dim]x{'-'*45}x[/dim]",
            "[dim]Based on Buckshot Roulette by Mike Klubnika[/dim]",
        ])

    @override 
    def key_q(self) -> None:
        self.app.exit()

class BoardView(_View):
    DEFAULT_CSS = """
    BoardView ContentWrapper {
        layout: grid;
        grid-size: 2 2;
        grid-rows: 60% 40%;
    }

    BoardView .sub-panel {
        width: 1fr;
        align: center top;
        border_top: solid white;
        border-title-align: center;
        padding: 1 2 1 2;
    }
    """

    # ---Internal Widgets---
    class Logs(RichLog, BuckshotEngine.BuckshotObserver):
        DEFAULT_CSS = """
        Logs {
            background: $background;
            padding: 1;
            column-span: 2;
        }

        Logs:focus {
            background: rgba(0, 0, 0, 0);
        }
        """

        message: reactive[str] = reactive("")

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__()
            engine.attach(self)

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            self.message = state.message
    
        def watch_message(self, old:str , new: str):
            if new and new != old:
                self.write(new)

    class Status(Widget, BuckshotEngine.BuckshotObserver):
        DEFAULT_CSS = """
        Status Horizontal {
            height: 2;
            align: center middle;
        }
        """

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(classes="sub-panel")
            engine.attach(self)
            self.border_title = " 󰷨 Board's Status "

        def compose(self) -> ComposeResult:
            attrs = [
                ("chamber", "Bullets Left:"),
                ("turn", "Current Turn:"),
                ("items-add", "Items Add:"),
                ("stage", "Stage:"),
            ]
            
            for id, label in attrs:
                with Horizontal():
                    yield Label(label)
                    yield Static("?", id=f"status-{id}", classes="right-align")

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            attrs = [
                ("chamber", "  ".join(["󰲅" * state.shotgun.bullets_left])),
                ("turn", state.players[state.turn].name),
                ("items-add", str(state.items_per_reload)),
                ("stage", state.stage),
            ]

            for query, value in attrs:
                self.query_one(f"#status-{query}", Static).update(value)

    class Players(Container, BuckshotEngine.BuckshotObserver):
        DEFAULT_CSS = """
        Players {
            layout: grid;
            grid-size: 1 2;
        }
        """

        class Player(Widget):
            pname: reactive[str]
            health: reactive[str]
            inventory: reactive[str]

            ICONS = {
                "magnifier": "󰍉",
                "beer": "󱄖",
                "cigarette": "󱆉",
                "handsaw": "󰹈",
                "handcuff": "󱄾"
            }

            DEFAULT_CSS = """
            Player .player-name {
                width: auto;
                padding-right: 1;
            }

            Player HorizontalGroup {
                padding-bottom: 1;
            }
            """

            def __init__(self, index: int, state: Player.PlayerState) -> None:
                super().__init__(id=f"player{index}")
                self.update(state)

            def compose(self) -> ComposeResult:
                with HorizontalGroup():
                    yield Label(f"{self.pname}:", id=f"{self.id}-pname", classes="player-name")
                    yield Static(self.health, id=f"{self.id}-health")
                yield Static("Empty", id=f"{self.id}-inventory")

            def update(self, state: Player.PlayerState) -> None:
                self.pname = state.name + ":"
                self.health = " ".join(["󱐋" * state.health])
                self.inventory = " | ".join(f"{self.ICONS[k]} {v}" for k, v in state.inventory.items())

            def on_mount(self):
                for attr in ["pname", "health", "inventory"]:
                    self.watch(self, attr, lambda v: self.query_one(f"#{self.id}-{attr}", Static).update(v))

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(classes="sub-panel")
            engine.attach(self)
            self.border_title = "  Player's Info "

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState) -> None:
            for idx, player in enumerate(state.players, start=1):
                try:
                    self.query_one(f"#player{idx}", self.Player).update(player)
                except NoMatches:
                    self.mount(self.Player(idx, player))

    # ---Player Interactive Prompt---
    class ActPrompt(_Prompt[list[str]]):
        class TargetPrompt(_Prompt[bool|None]):
            BINDINGS = [
                ("0", "dismiss(True)", "Shoot yourself"),
                ("1", "dismiss(False)", "Shoot opponent"),
            ]

        def __init__(self, caller: BoardView) -> None:
            super().__init__()
            self.caller = caller
            self.engine = caller._engine

        def on_mount(self):
            available_items = [k for k, v in self.engine._players[self.engine._turn].inventory.items.items() if v > 0]

            self._bindings.bind("0", "parse_item('gun')", "Use Gun")
            for key, name in enumerate(available_items, start=1):
                self._bindings.bind(str(key), f"parse_item('{name}')", f"Use {name}")

        @work
        async def action_parse_item(self, item: str):
            if item not in self.engine._valid_actions:
                return

            logs = self.caller.query_one(BoardView.Logs)
    
            actions = [item]
            if item == "gun":
                logs.write(" | ".join(["󱆉", "󱄾", "󰍉", "󱄖", "󰹈"]))
                target = "self" if await self.app.push_screen_wait(self.TargetPrompt()) else "opponent"
                actions.append(target)

            self.dismiss(actions)

        @override
        def key_q(self):
            self.dismiss([''])

    class ConfirmPrompt(_Prompt[bool]):
        DEFAULT_CLASSES = "hidden-prompt"
        BINDINGS = []

    class SetupPrompt(_Prompt[tuple[str, ...]]):
        #TODO: change setup prompt to normal screen

        def compose(self) -> ComposeResult:
            yield Label("Enter player's names:")
            yield Input(compact=True, max_length=5, id="input01")
            yield Input(compact=True, max_length=5, id="input02")

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

    NAME = 'board'
    BINDINGS = [
        ("space", "act"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._engine = BuckshotEngine()

    def assign(self) -> ComposeResult:
        yield from (widget(self._engine) for widget in [self.Logs, self.Status, self.Players])

    @work
    async def on_mount(self):
        if not self._engine.ready: # ensure that engine has been created for game to load
            self._engine.setup(*await self.app.push_screen_wait(self.SetupPrompt()))
        self._engine.reset(hard=True) # reload new game but keeping player's names

    @work
    async def action_act(self):
        self._engine.execute(await self.app.push_screen_wait(self.ActPrompt(self)))

class HelpView(_View):
    NAME = 'help'
    def assign(self) -> ComposeResult:
        yield Static("This is a help screen")

class CreditView(_View):
    NAME = 'credit'
    def assign(self) -> ComposeResult:
        yield Static("This is a credit screen")

# ---Main App---
class BuckshotApp(App): 
    ENABLE_COMMAND_PALETTE = False
    TITLE = "BUCKSHOTxROULETTE"
    ENGINE: BuckshotEngine
    MODES = {view.NAME: view for view in [TitleView, BoardView, HelpView, CreditView]}
    BINDINGS = [
        Binding("h", "app.switch_mode('help')", priority=True),
        Binding("c", "app.switch_mode('credit')", priority=True),
    ]

    def on_mount(self):
        def get_version():
            try:
                return version("buckshot-roulette")
            except PackageNotFoundError:
                return "Unknown"

        self.sub_title = get_version()
        self.switch_mode('title')

    def on_resize(self):
        #TODO: create a function to calculate the width and height for the app so that the aspect ratio always return 2
        # if not push a screen that cover everything
        pass


