from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version

from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer

from buckshot.engine import BuckshotEngine
from buckshot.widget import *

# ---Main App---
class BuckshotApp(App): 
    ENABLE_COMMAND_PALETTE = False
    TITLE = "BUCKSHOTxROULETTE"
    ENGINE: BuckshotEngine
    AUTO_FOCUS = "PlayerInput Input"

    DEFAULT_CSS = """
    ScrollableContainer {
        overflow: auto auto;
        align: center middle;
        scrollbar-background: $background;
        scrollbar-background-active: $background;
        scrollbar-background-hover: $background;
        scrollbar-corner-color: $background;
        scrollbar-color: $background;
        scrollbar-color-active: white;
        scrollbar-color-hover: white;
        scrollbar-size: 1 1;
    }

    .right-align {
        content-align: right middle;
    }
    """

    def __init__(self):
        super().__init__()
        self.sub_title = self.version
        self.ENGINE = BuckshotEngine()
        self.players: list[str] = []

    @property
    def version(self):
        try: 
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with GameContainer():
                yield BoardView(self.ENGINE)
                yield PlayerInput()

    def write(self, mess: str, type: str = ""):
        #TODO: add output type (err, info, warn, etc.)
        self.query_one(BoardView.Logs).write(mess)

    def clear(self):
        self.query_one(BoardView.Logs).clear()

    def on_mount(self):
        if not self.ENGINE.ready:
            self.write("This is a contract, sign it!")
            return

        self.ENGINE.reset(hard=True)

    def key_enter(self):
        self.query_one("PlayerInput Input").focus()

    @on(PlayerInput.Submitted)
    def execute(self, event: PlayerInput.Submitted) -> None:
        match event.action:
            case "sign":
                self.ENGINE.sign(event.args[0])
            case "clear":
                self.clear()
            case "exit":
                self.exit()
            case "use":
                self.ENGINE.execute(*event.args)
            case "shoot":
                self.write("Player shoot Dealer!")
            case _:
                self.write("Error: Invalid command. Try <help> for a list of available commands.")
