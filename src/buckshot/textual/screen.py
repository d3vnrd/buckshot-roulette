from typing import override

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import (
    Label,
    Footer,
)
from textual.containers import (
    Vertical
)

from .widget import *

class DefaultScreen(Screen):
    BINDINGS = [
        ("q", "app.quit", "Exit"),
        ("h", "app.switch_mode('help')", "Help"),
        ("s", "app.switch_mode('setting')", "Setting"),
        ("space", "app.switch_mode('board')", "Setup")
    ]

    @override
    def compose(self) -> ComposeResult:
        with Vertical():
            yield TitleScreen()
            yield Footer()

class MainGameScreen(Screen):
    BINDINGS = [
        ("q", "app.switch_mode('default')", "Back to default"),
        ("space", "player_interact", "Interact")
    ]

    @override
    def compose(self) -> ComposeResult:
        yield Label("This is the main game view.")
        yield Footer(show_command_palette=False)

class HelpScreen(ModalScreen):
    BINDINGS = [("q", "app.switch_mode('default')", "Back to default")]
    @override
    def compose(self) -> ComposeResult:
        yield Label("This is the help screen")
        yield Footer(show_command_palette=False)

class SettingScreen(ModalScreen):
    BINDINGS = [("q", "app.switch_mode('default')", "Back to default")]
    @override
    def compose(self) -> ComposeResult:
        yield Label("This is the setting screen")
        yield Footer(show_command_palette=False)

