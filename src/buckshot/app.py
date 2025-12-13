from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar, override
from importlib.metadata import PackageNotFoundError, version

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, HorizontalGroup, ScrollableContainer
from textual.css.query import NoMatches
from textual.message import Message
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
from buckshot.entity import Dealer, Player

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
        yield Footer()

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

    class Write(Message):
        def __init__(self, mess: str) -> None:
            self.mess = mess
            super().__init__()

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
    class Logs(RichLog, BuckshotEngine.BuckshotObserver):
        DEFAULT_CSS = """
        Logs {
            background: $background;
            border: round white;
            margin: 0 1 0 1;
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
        Status {
            border_right: solid white;
        }

        Status HorizontalGroup {
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

    class Players(Container, BuckshotEngine.BuckshotObserver):
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
            # TODO: move this to inner engine
            ICONS = {"magnifier": "󰍉", "beer": "󱄖", "cigarette": "󱆉", "handsaw": "󰹈", "handcuff": "󱄾" }

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
                def make_watcher(attr: str):
                    def update(value: str):
                        self.query_one(f"#{self.id}-{attr}", Static).update(value)
                    return update

                for attr in ["pname", "health", "inventory"]:
                    self.watch(self, attr, make_watcher(attr))

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(classes="sub-panel")
            engine.attach(self)
            self.border_title = "  Player's Info "

        def compose(self) -> ComposeResult:
            yield self.Register()

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState) -> None:
            try:
                self.query_one(self.Register).remove()
            except NoMatches:
                pass

            for idx, player in enumerate(state.players, start=1):
                try:
                    self.query_one(f"#player{idx}", self.Player).update(player)
                except NoMatches:
                    self.mount(self.Player(idx, player))

    # ---Player Interactive Hidden Prompt---
    class ConfirmPrompt(_Prompt[bool]):
        BINDINGS = [
            ("y", "dismiss(True)"),
            ("n", "dismiss(False)")
        ]

        def __init__(self, mess:str = "Are you sure?") -> None:
            super().__init__()
            self.mess = mess

        def on_mount(self):
            self.screen.query_one(BoardView.Logs).write(self.mess + " (y/n):")

        @override
        def key_q(self):
            self.dismiss(False)

    class ActPrompt(_Prompt[list[str]]):
        class TargetPrompt(_Prompt[bool|None]):
            BINDINGS = [
                ("0", "dismiss(True)", "Shoot yourself"),
                ("1", "dismiss(False)", "Shoot opponent"),
            ]

        def __init__(self, player: Player.PlayerState) -> None:
            self.player: Player.PlayerState = player
            super().__init__()

        def on_mount(self):
            available_items = [k for k, v in self.player.inventory.items() if v > 0]

            self._bindings.bind("0", "parse_item('gun')", "Use Gun")
            for key, name in enumerate(available_items, start=1):
                self._bindings.bind(str(key), f"parse_item('{name}')", f"Use {name}")

        @work
        async def action_parse_item(self, item: str):
            actions = [item]
            if item == "gun":
                self.post_message(self.Write("Player picked up the gun, and wondering who to shoot?"))
                target = "self" if await self.app.push_screen_wait(self.TargetPrompt()) else "opponent"
                actions.append(target)

            self.dismiss(actions)

        @override
        def key_q(self):
            self.dismiss([''])

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

    def __init__(self) -> None:
        super().__init__()
        self._engine = BuckshotEngine() # mount ui to underlying engine
        self.players: list[str] = []

    def assign(self) -> ComposeResult:
        yield from (widget(self._engine) for widget in [self.Logs, self.Status, self.Players])

    def on_mount(self):
        if not self._engine.ready: # ensure that engine has been created for game to load
            #TODO: update the contract
            self.query_one(self.Logs).write("Here is the contract, sign it by entering your name!")
            self.query_one(Input).focus()
            return

        self._engine.reset(hard=True) # reload new game but keeping player's names

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

        self._engine.setup(*self.players)
        self._engine.reset(hard=True)

    @work
    async def key_space(self):
        self._engine.execute(await self.app.push_screen_wait(self.ActPrompt(self._engine._players[self._engine._turn].state)))

    def on_act_prompt_write(self, message: ActPrompt.Write) -> None:
        self.query_one(self.Logs).write(message.mess)

    def check_action_space(self):
        return isinstance(self._engine._players[self._engine._turn], Dealer)

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


