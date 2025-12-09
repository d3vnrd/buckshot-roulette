from __future__ import annotations
from abc import abstractmethod
from importlib.metadata import PackageNotFoundError, version
from typing import TypeVar, override

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, ScrollableContainer
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import (
    RichLog,
    Static
)

from buckshot.engine import BuckshotEngine

T = TypeVar("T")

class BuckshotApp(App): 
    class Prompt(ModalScreen[T]):
        BINDINGS = [('escape', 'dismiss')]
        DEFAULT_CSS = """
        Prompt {}
        """

    class MainScreen(Container, BuckshotEngine.BuckshotObserver):
        DEFAULT_CSS = """
        MainScreen {
            width: 1fr;
            column_span: 2;
            align: center middle;
        }
        """

        class TitleView(ScrollableContainer):
            DEFAULT_CSS = """
            TitleView {
                width: 60%;
                height: 1fr;
                align: center middle;
            }

            TitleView Static {
                width: 1fr;
                height: 1;
            }
            """

            def compose(self) -> ComposeResult:
                yield Static("Title", id="title")
                yield Static("<space> Start", id="start")

            @abstractmethod
            def on_update(self, state: BuckshotEngine.BuckshotState) -> None:
                pass

        class BoardView(TitleView):
            DEFAULT_CSS = """
            BoardView {
                layout: grid;
                grid-size: 2;
            }
            """

            chamber: reactive[str] = reactive("?")
            turn: reactive[str] = reactive("?")
            items: reactive[str] = reactive("?")
            stage: reactive[str] = reactive("?")

            @override
            def compose(self) -> ComposeResult:
                yield Static("Bullets Left:")
                yield Static(self.chamber, id="status-chamber")
                yield Static("Current Turn:")
                yield Static(self.turn, id="status-turn")
                yield Static("Items per reload:")
                yield Static(self.items, id="status-items")
                yield Static("Stage:")
                yield Static(self.stage, id="status-stage")

            @override
            def on_update(self, state: BuckshotEngine.BuckshotState) -> None:
                self.chamber = str(state.shotgun.bullets_left)
                self.turn = state.players[state.turn].name
                self.items = str(state.items_per_reload)
                self.stage = state.stage

            def on_mount(self):
                for attr in ["chamber", "turn", "items", "stage"]:
                    self.watch(
                        self, attr, 
                        lambda v: self.query_one(f"#status-{attr}", Static).update(v)
                    )

        class HelpView(TitleView):
            @override
            def compose(self) -> ComposeResult:
                yield Static("Help", id="help-title")
                yield Static("Use keys wisely", id="help-text")

        class CreditView(TitleView):
            @override
            def compose(self) -> ComposeResult:
                yield Static("Credit", id="credit-title")
                yield Static("Made by meh!", id="credit-text")

        # Reactive var to change board view: title, board, help, credit
        view: reactive[str] = reactive('title', recompose=True)

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__()
            engine.attach(self)

        def compose(self) -> ComposeResult:
            match self.view:
                case 'board':
                    yield self.BoardView()
                case 'credit':
                    yield self.CreditView()
                case 'help':
                    yield self.HelpView()
                case _:
                    yield self.TitleView()

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState) -> None:
            try:
                self.query_one(self.BoardView).on_update(state)
            except NoMatches:
                return

    class Logs(RichLog, BuckshotEngine.BuckshotObserver):
        message: reactive[str] = reactive("")

        DEFAULT_CSS = """
        Logs {
            background: $background;
            padding: 1;
        }

        Logs:focus {
            background: rgba(0, 0, 0, 0);
        }
        """

        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(classes="panel")
            engine.attach(self)
            self.border_title = " 󰷨 Logs "

        @override
        def on_engine_update(self, state: BuckshotEngine.BuckshotState):
            self.message = state.message
    
        def watch_message(self, old:str , new: str):
            if new and new != old:
                self.query_one("#logs", RichLog).write(new)

    class PlayersInventory(Container, BuckshotEngine.BuckshotObserver):
        def __init__(self, engine: BuckshotEngine) -> None:
            super().__init__(classes="panel")
            engine.attach(self)
            self.border_title = "  Player's Info "

        def compose(self) -> ComposeResult:
            return super().compose()

    ENABLE_COMMAND_PALETTE = False

    DEFAULT_CSS = """
    #content {
        width: 80;
        height: 40;
        border: ascii white;
        border-title-align: center;
        border-subtitle-align: right;
        layout: grid;
        grid-size: 2 2;
    }

    #wrapper {
        overflow: auto auto;
        align: center middle;
    }

    .panel {
        border_top: ascii white;
        border-title-align: center;
    }

    ScrollableContainer {
        scrollbar-background: $background;
        scrollbar-background-active: $background;
        scrollbar-background-hover: $background;
        scrollbar-corner-color: $background;
        scrollbar-color: $background;
        scrollbar-color-active: white;
        scrollbar-color-hover: white;
        scrollbar-size: 1 1;
    }
    """

    BINDINGS = [
        Binding(*key) for key in [
            ('h', "change_view('help')"),
            ('space', "change_view('board')"),
            ('q', "exit"),
            *[(str(i), f"parse_item('{name}')") for i, name in enumerate(
                ["magnifier", "beer", "handsaw", "cigarette", "handcuff"],
                start=1
            )],
        ]
    ]

    _engine = BuckshotEngine('', '')

    def compose(self) -> ComposeResult:
        elems = (widget(self._engine) for widget in [self.MainScreen, self.Logs, self.PlayersInventory])
        yield ScrollableContainer(Container(*elems, id="content"), id="wrapper")

    def on_mount(self):
        def buckshot_version():
            try:
                return version("buckshot-roulette")
            except PackageNotFoundError:
                return "Unknown"

        content = self.query_one("#content")
        content.border_title = "󰍉 󱄾 BUCKSHOTxROULETTE 󱆉 󰹈"
        content.border_subtitle = f"v{buckshot_version()}"

    def on_resize(self):
        #TODO: create a function to calculate the width and height for the app so that the aspect ratio always return 2
        pass

    def action_change_view(self, view: str = 'title'):
        self.query_one(self.MainScreen).view = view

    def action_exit(self):
        if self.query_one(self.MainScreen).view == 'title':
            self.exit() 
        else:
            self.action_change_view()

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        return True if (
            action in [""], 
            self.query_one(self.MainScreen).view == 'board'
        ) else False

