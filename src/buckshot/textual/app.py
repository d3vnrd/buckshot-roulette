from importlib.metadata import PackageNotFoundError, version
from .elem import *
from .screen import *
from textual.app import App
from buckshot.board import Board

class BuckshotApp(App): 
    ENABLE_COMMAND_PALETTE = False

    DEFAULT_MODE = "default"
    MODES = {
        "default": DefaultScreen,
        "credit": CreditScreen,
        "help": HelpScreen,
        "setup": SetupScreen,
        "board": MainGameScreen
    }

    def __init__(self, args: list[str] | None = None):
        super().__init__()
        self.board: Board = Board()
        self.app.title = "buckshot-roulette"
        self.app.sub_title = f"v{self.get_version()}"

    def get_version(self):
        try:
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"
