from __future__ import annotations
from typing import TYPE_CHECKING

from .widget import *
from .screen import *
from textual.app import App

if TYPE_CHECKING:
    from buckshot import Board

class BuckshotApp(App): 
    CSS_PATH = "asset/style.tcss"
    ENABLE_COMMAND_PALETTE = False

    DEFAULT_MODE = "default"
    MODES = {
        "default": DefaultScreen,
        "setting": SettingScreen,
        "help": HelpScreen,
        "board": MainGameScreen
    }

    def __init__(self, board: Board):
        super().__init__()
        self.board: Board = board

    def on_mount(self):
        pass
