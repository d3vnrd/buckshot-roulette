from typing import override

from textual.app import ComposeResult
from textual.containers import (
    Center, 
    CenterMiddle,
    HorizontalGroup,
    Vertical, 
    VerticalGroup
)
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    Label,
)

class TitleScreen(VerticalGroup):
    @override
    def compose(self) -> ComposeResult:
        with CenterMiddle():
            yield Center(Label("BUCKSHOTxROULETTE", id="game-title"))
            yield Center(Label(f"x{"-"*45}x"))
            yield Center(Label("Based on Buckshot Roulette by Mike Klubnika", classes="game-subtitle"))
            yield Center(Label("Press <Space> to continue", classes="game-subtitle"))

class GameSetting(ModalScreen):
    @override
    def compose(self) -> ComposeResult:
        with Vertical(id="setting-screen"):
            yield Label("Settings", id="setting-screen-title")
            
            with HorizontalGroup(id="button-group"):
                yield Button("Save", compact=True, variant="primary", id="setting-save-btn")
                yield Button("Cancel", compact=True, variant="default", id="setting-cancel-btn")

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "setting-save-btn":
                self.dismiss()
            case "setting-cancel-btn":
                self.dismiss()
            case _:
                pass
