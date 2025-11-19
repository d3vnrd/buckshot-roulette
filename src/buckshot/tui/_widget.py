from typing import override

from textual.app import ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical
from textual.widget import Widget
from textual.widgets import (
    Label,
    Log,
    ProgressBar,
)

class Header(Horizontal):
    @override
    def compose(self) -> ComposeResult:
        yield Label(f"[dim]{self.app.title} - {self.app.sub_title}[/dim]")
        yield Label("[dim]13:10:58[/dim]", classes="right-align")

class GameTitle(Vertical):
    @override
    def compose(self) -> ComposeResult:
        yield Label("[bold orange]BUCKSHOTxROULETTE[/bold orange]", id="title")
        yield Label(f"[dim]x{'-'*45}x[/dim]", id="divider")
        yield Label("[dim]Based on Buckshot Roulette by Mike Klubnika[/dim]", classes="other")
        yield Label("[dim]Press <Space> to continue[/dim]", classes="other")

class PlayersInfo(Widget):
    def __init__(self) -> None:
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        for player in ["Player 1", "Player 2"]:
            with Container(classes="player-cards"):
                yield Label(player, classes="pane-title")
                with HorizontalGroup():
                    yield Label("Health: ")
                    yield ProgressBar(
                        total=8, 
                        show_percentage=False,
                        show_eta=False, 
                        classes="right-align"
                    )
                with HorizontalGroup():
                    yield Label("Total Items: ")
                    yield Label("10", classes="right-align")

class PlayersInventory(Widget):
    @override
    def compose(self) -> ComposeResult:
        yield Label("Detail Inventory", classes="pane-title")

class GameStatus(Widget):
    @override
    def compose(self) -> ComposeResult:
        yield Label("Game Status", classes="pane-title")
        with HorizontalGroup():
            yield Label("Gun Chamber: ")
            yield ProgressBar(total=8, show_percentage=False, show_eta=False, classes="right-align")

        with HorizontalGroup():
            yield Label("Current Turn: ")
            yield Label("Player 1", classes="right-align")

        with HorizontalGroup():
            yield Label("Items Per Reload: ")
            yield Label("2", classes="right-align")

        with HorizontalGroup():
            yield Label("Live Shells: ")
            yield Label("3", classes="right-align")

        with HorizontalGroup():
            yield Label("Stage: ")
            yield Label("I", classes="right-align")

class GameLogs(Widget):
    @override
    def compose(self) -> ComposeResult:
        yield Label("Logs", classes="pane-title")
        yield Log()

class GameChats(Widget):
    @override
    def compose(self) -> ComposeResult:
        yield Label("Chats", classes="pane-title")
        yield Log()
