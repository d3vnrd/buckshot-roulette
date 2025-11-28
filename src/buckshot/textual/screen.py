from typing import override
from buckshot import BuckshotEngine

from textual import on
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import (
    Footer,
    Input,
    Label,
)

# ---Popup-Screens for Player Interactions---
class ConfirmExit(ModalScreen[bool]):
    BINDINGS = [
        ("y", "dismiss(True)", "yes"),
        ("n", "dismiss(False)", "no"),
    ]

    @override
    def compose(self) -> ComposeResult:
        yield Label("Are you sure you want to exit?:")
        yield Footer(compact=True)

class SetupScreen(ModalScreen[tuple]):
    @override
    def compose(self) -> ComposeResult:
        yield Label("Enter player's names:")
        yield Input(compact=True, max_length=8, id="input01")
        yield Input(compact=True, max_length=8, id="input02")

    @on(Input.Submitted, "#input01")
    def next(self):
        self.set_focus(self.query_one("#input02"))

    @on(Input.Submitted, "#input02")
    def confirm_setup(self):
        if not self.query_one("#input01", Input).value:
            self.set_focus(self.query_one("#input01"))
            return

        p01name = self.query_one("#input01", Input).value
        p02name = self.query_one("#input02", Input).value
        self.dismiss((p01name, p02name))


class PlayerActionsHandler(ModalScreen[list[str]]):
    BINDINGS = [
        ("q", "dismiss", "Cancel"),
    ]

    def __init__(self, state: BuckshotEngine.BuckshotState) -> None:
        self.state = state
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        yield Footer(compact=True)

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        pass

