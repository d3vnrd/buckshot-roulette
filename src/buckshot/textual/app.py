from importlib.metadata import PackageNotFoundError, version
from typing import override
from abc import abstractmethod

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import (
    Container,
)
from textual.widgets import (
    Footer,
)

from .widget import *

# ---Main Panels---
class BaseScreen(Screen):
    BINDINGS = [("q", "app.switch_mode('default')", "Back")]

    @override
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id='main-contents'):
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
        ("space", "enter_game", "Start")
    ]

    @override
    def set_content(self):
        yield GameTitle()

    def action_enter_game(self):
        self.app.push_screen(MainGameScreen())

class HelpScreen(BaseScreen):
    @override
    def set_content(self) -> ComposeResult:
        yield Label("Loading help content...")

class CreditScreen(BaseScreen):
    @override
    def set_content(self) -> ComposeResult:
        yield Label("This is the credit screen")

class MainGameScreen(BaseScreen):
    _engine = BuckshotEngine()

    BINDINGS = []

    @override
    def set_content(self) -> ComposeResult:
        yield GameLogs(self._engine)
        yield PlayersInfo(self._engine)

# ---Buckshot App---
class TextualBuckshot(App): 
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = [
        "./style/main.tcss",
        "./style/widget.tcss",
    ]

    DEFAULT_MODE = "default"
    MODES = {
        "default": DefaultScreen,
        "credit": CreditScreen,
        "help": HelpScreen,
    }

    def __init__(self, args: list[str] | None = None):
        super().__init__()
        self.app.title = "buckshot-roulette"
        self.app.sub_title = f"v{self.get_version()}"

    def get_version(self):
        try:
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"
