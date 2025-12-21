from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar, override
from importlib.metadata import PackageNotFoundError, version

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, HorizontalGroup, ScrollableContainer
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

T = TypeVar("T")

class _View(Screen[T]):
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

class _Prompt(ModalScreen[T]):
    DEFAULT_CSS = """
    _Prompt {
        background: rgba(0, 0, 0, 0)
    }
    """

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
    # ---Internal Widgets---
    class LogsPanel(RichLog, BuckshotEngine.BuckshotObserver):
        DEFAULT_CSS = """
        LogsPanel {
            background: $background;
            border: round white;
            margin: 0 1 0 1;
            padding: 1;
            column-span: 2;
        }

        LogsPanel:focus {
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

    class StatusPanel(Widget, BuckshotEngine.BuckshotObserver):
        DEFAULT_CSS = """
        StatusPanel {
            border_right: solid white;
        }

        StatusPanel HorizontalGroup {
            height: 1;
            margin-bottom: 1;
            align: center middle;
        }
        """

        chamber: reactive[str] = reactive("?")
        turn: reactive[str] = reactive("?")
        items: reactive[str] = reactive("?")
        stage: reactive[str] = reactive("?")

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(classes="sub-panel")
            engine.attach(self)
            self.border_title = " 󰷨 Board's Status "

        def compose(self) -> ComposeResult:
            for label, attr in [
                ("Bullets Left:", "chamber"),
                ("Current Turn:", "turn"),
                ("Items Add:", "items"),
                ("Stage:", "stage"),
            ]:
                with HorizontalGroup():
                    yield Label(label)
                    yield Static(getattr(self, attr), id=f"status-{attr}", classes="right-align")

        def on_mount(self) -> None:
            def make_watcher(attr: str):
                def update(value: str):
                    self.query_one(f"#status-{attr}", Static).update(value)
                return update

            for attr in ["chamber", "turn", "items", "stage"]:
                self.watch(self, attr, make_watcher(attr))

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            self.chamber = " ".join(["󰲅"] * state.shotgun.bullets_left)
            self.turn = state.players[state.turn].name
            self.items = str(state.items_per_reload)
            self.stage = state.stage

    class PlayerPanel(Container, BuckshotEngine.BuckshotObserver):
        class Register(Widget):
            DEFAULT_CSS = """
            Register Input {
                width: 1fr;
                margin-top: 1;
            }

            Register Input:focus {
                background: rgba(0, 0, 0, 0);
            }
            """
            def compose(self) -> ComposeResult:
                yield Static("Enter Player's Name:")
                yield Input(compact=True, max_length=8)

            #TODO: add value checker exclude name like GOD, DEALER, > 8

        class Player(Widget):
            ICONS = {
                "magnifier": "󰍉", 
                "beer": "󱄖", 
                "cigarette": "󱆉", 
                "handsaw": "󰹈", 
                "handcuff": "󱄾",
            }

            DEFAULT_CSS = """
            Player {
                height: auto;
                width: 1fr;
                padding-bottom: 1;
            }

            Player .player-name {
                width: auto;
                padding-right: 1;
            }

            Player HorizontalGroup {
                padding-bottom: 1;
            }
            """

            pname: reactive[str]
            health: reactive[str]
            inventory: reactive[str]

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
                def w_func(attr: str):
                    return lambda v: self.query_one(f"#{self.id}-{attr}", Static).update(v)

                for attr in ["pname", "health", "inventory"]:
                    self.watch(self, attr, w_func(attr))

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(classes="sub-panel")
            engine.attach(self)
            self.border_title = "  Player's Info "

        def compose(self) -> ComposeResult:
            yield self.Register()

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState) -> None:
            for idx, player in enumerate(state.players, start=1):
                try:
                    self.query_one(f"#player{idx}", self.Player).update(player)
                except NoMatches:
                    self.mount(self.Player(idx, player))

    # --Support Interaction Prompt---
    class TargetPrompt(_Prompt[bool]):
        BINDINGS = [
            ("space", "dismiss(False)"),
            ("1", "dismiss(True)")
        ]

        @override
        def key_q(self):
            self.dismiss(False)

    # ---BoardView's Main Logic---
    NAME = 'board'
    DEFAULT_CSS = """
    BoardView ContentWrapper {
        layout: grid;
        grid-size: 2 2;
        grid-rows: 70% 30%;
    }

    BoardView .sub-panel {
        width: 1fr;
        align: center top;
        border_top: solid white;
        border-title-align: center;
        padding: 1 2 1 2;
    }
    """

    BINDINGS = [
        ("space", "parse_item('gun')"),
        *[(str(i), f"parse_item('{name}')") for i, name in enumerate(
            ["magnifier", "beer", "handsaw", "cigarette", "handcuff"],
            start=1
        )]
    ]

    def __init__(self) -> None:
        super().__init__()
        self._engine = BuckshotEngine() # mount UI to underlying engine
        self.players: list[str] = []

    def assign(self) -> ComposeResult:
        yield from (widget(self._engine) for widget in [self.LogsPanel, self.StatusPanel, self.PlayerPanel])
        yield Footer()

    def on_mount(self):
        if not self._engine.ready: # ensure that engine has been created for game to load
            self.query_one(self.LogsPanel).write("Here is the contract, sign it by entering your name!") #TODO: update the contract
            self.query_one(Input).focus()
            return

        self._engine.reset(hard=True) # reload new game but keeping player's names

    def write(self, mess: str) -> None:
        self.query_one(self.LogsPanel).write(mess)

    @on(Input.Submitted)
    def _add_player(self):
        inputer = self.query_one(Input)

        if inputer.value != "":
            self.players.append(inputer.value)
            inputer.value = ""
            inputer.focus()
            return 

        if len(self.players) == 1:
            self.players.append("Dealer")

        self.query_one(self.PlayerPanel.Register).remove() # replace Register with actual Player's information
        self._engine.setup(*self.players)
        self._engine.reset(hard=True)

    @work
    async def action_parse_item(self, item: str):
        actions: list[str] = [item]
        if item == "gun":
            self.write("You picked up the gun, wonder who to shoot? (space: self | 1: opponent)")
            target = "opponent" if await self.app.push_screen_wait(self.TargetPrompt()) else "self"
            actions.append(target)

        self._engine.execute(actions)

    @override
    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        for key in range(1, 6):
            if action == key:
                return self._engine._players[self._engine._turn].inventory.has_item(parameters[0])

        return True


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


