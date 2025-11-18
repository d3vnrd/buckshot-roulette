from typing import override

from textual.app import ComposeResult
from textual.containers import Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.widgets import (
    Label,
    Log,
    ProgressBar,
    Static,
)

from buckshot.entity import Player

class Header(Horizontal):
    DEFAULT_CSS = """
    #version {
        width: 50%;
    }

    #timer {
        width: 50%;
        content-align: right middle;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        yield Label(f"[dim]{self.app.title} - {self.app.sub_title}[/dim]", id="version")
        yield Label("[dim]13:10:58[/dim]", id="timer")

class GameTitle(Vertical):
    DEFAULT_CSS = """
    GameTitle { 
        align: center middle; 
    }

    GameTitle Label {
        width: 100%;
        height: auto;
        content-align: center middle;
    }
    """
    
    @override
    def compose(self) -> ComposeResult:
        yield Label("[bold orange]BUCKSHOTxROULETTE[/bold orange]")
        yield Label(f"[dim]x{'-'*45}x[/dim]")
        yield Label("[dim]Based on Buckshot Roulette by Mike Klubnika[/dim]")
        yield Label("[dim]Press <Space> to continue[/dim]")

class PlayersInfo(VerticalScroll):
    DEFAULT_CSS = """
    .player-card {
        height: 50%;
        align: center middle;
        margin-right: 1;
    }
    """

    def __init__(self, players: list[Player] | None = None) -> None:
        self.players: list[Player] | None = players
        super().__init__()

    @override
    def compose(self) -> ComposeResult:
        #TODO: use iterator for this
        with VerticalGroup(classes="player-card"):
            yield Label("[b orange]Player 1[/b orange]", classes="pane-title")
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


        with VerticalGroup(classes="player-card"):
            yield Label("[b orange]Player 2[/b orange]", classes="pane-title")
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

class GameStatus(Vertical):
    DEFAULT_CSS = """
    GameStatus {
        width: 100%;
        height: 100%;
        align: center middle;
        margin-left: 1;
    }
    """

    @override
    def compose(self) -> ComposeResult:
        yield Label("[b orange]Game Status[/b orange]", classes="pane-title")
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

class GameLogs(Static):
    
    DEFAULT_CSS = """
    GameLogs {
        width: 1fr;
        height: 15;
        content-align: center middle;
        column-span: 2;
    }

    GameLogs Log {
        background: $background;
        scrollbar-visibility: hidden;
    }

    GameLogs Label {
        text-align: center;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("[b orange]Current game logs[/]", classes="pane-title")
        yield Log()


class GameChats(Static):
    DEFAULT_CSS = """
    GameChats {
        width: 1fr;
        height: 1fr;
        content-align: center middle;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("[b orange]Game chats[/]", classes="pane-title")
        yield Log()


class DetailInventory(Static):
    DEFAULT_CSS = """
    DetailInventory {
        width: 1fr;
        height: 1fr;
        content-align: center middle;
    }
    """
    
    def compose(self) -> ComposeResult:
        yield Label("[b orange]Detail inventory[/]", classes="pane-title")
