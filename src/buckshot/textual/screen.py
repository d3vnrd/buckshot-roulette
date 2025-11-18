from abc import abstractmethod
from typing import override

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import (
    Label,
    Footer,
)

from .elem import *

class BaseScreen(Screen):
    BINDINGS = [("q", "app.switch_mode('default')", "Back")]

    DEFAULT_CSS = """
    BaseScreen {
        layout: vertical;
    }

    BaseScreen Header {
        width: 100%;
        height: 1;
        padding: 0 1 0 1;
    }

    BaseScreen Container {
        width: 100%;
        height: 1fr;
        padding: 0 1 0 1;
    }

    BaseScreen Footer {
        align: right middle;
        background: $background;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="content"):
            yield from self.set_content()
        yield Footer()

    @abstractmethod
    def set_content(self) -> ComposeResult: 
        pass

class DefaultScreen(BaseScreen):
    BINDINGS = [
        ("q", "app.quit", "Exit"),
        ("h", "app.switch_mode('help')", "Help"),
        ("c", "app.switch_mode('credit')", "Credit"),
        ("space", "app.switch_mode('setup')", "Setup")
    ]

    @override
    def set_content(self):
        yield GameTitle()

class HelpScreen(BaseScreen):
    @override
    def set_content(self) -> ComposeResult:
        yield Label("Loading help content...")

class CreditScreen(BaseScreen):
    @override
    def set_content(self) -> ComposeResult:
        yield Label("This is the credit screen")

class SetupScreen(BaseScreen):
    BINDINGS = [
        *BaseScreen.BINDINGS,
        ("space", "app.switch_mode('board')", "Confirm")
    ]

    @override
    def set_content(self) -> ComposeResult:
        yield Label("This is the setup screen")

class MainGameScreen(BaseScreen):
    BINDINGS = [
        ("q", "app.switch_mode('setup')", "Back to setup"),
        ("space", "player_interact", "Interact")
    ]

    DEFAULT_CSS = """
    MainGameScreen Container {
        width: 100%;
        height: 1fr;
        layout: grid;
        grid-size: 2 3;
    }

    MainGameScreen Log {
        background: $background;
        scrollbar-visibility: hidden;
    }

    .pane-title { 
        width: 100%;
        margin-bottom: 1;
        content-align: center middle;
    }

    .right-align {
        width: 1fr;
        align: right middle;
        content-align: right middle;
    }
    """

    @override
    def set_content(self) -> ComposeResult:
       # Top section: Players info + Game status
        yield PlayersInfo()
        yield GameStatus()
        
        # Middle section: Game logs
        yield GameLogs()
        
        # Bottom section: Game chats + Detail inventory
        yield GameChats()
        yield DetailInventory()


