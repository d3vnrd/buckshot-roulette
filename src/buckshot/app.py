from __future__ import annotations
from abc import abstractmethod
from typing import TypeVar
from importlib.metadata import PackageNotFoundError, version

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen
from textual.widget import Widget

from buckshot.engine import BuckshotEngine
from buckshot.widget import *

T = TypeVar("T")

class _View(Screen[T]):
    DEFAULT_CSS = """
    _View ScrollableContainer {
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

    _View Static {
        width: 1fr;
        height: 1;
    }

    _View .center-align {
        content-align: center middle;
    }

    _View .right-align {
        content-align: right middle;
    }
    """

    NAME: str

    class ContentWrapper(Container):
        DEFAULT_CSS = """
        ContentWrapper {
            width: 80;
            height: 40;
            border: round white;
            border-title-align: center;
            border-subtitle-align: right;
            align: center middle;
        }
        """

        def __init__(self, *children: Widget) -> None:
            super().__init__(*children)
            self.border_title = f"󰍉 󱄾 {self.app.title} 󱆉 󰹈"
            self.border_subtitle = f"v{self.app.sub_title}"

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with self.ContentWrapper():
                yield from self.assign()

    @abstractmethod
    def assign(self) -> ComposeResult:
        pass

class BoardView(_View):
    NAME = 'board'

    def __init__(self) -> None:
        super().__init__()
        self._engine = BuckshotEngine() # mount UI to underlying engine
        self.players: list[str] = []

    def assign(self) -> ComposeResult:
        yield GameStatus(self._engine)
        yield CmdsInput(self._engine)

    def on_mount(self):
        if not self._engine.ready: # ensure that engine has been created for game to load
            self.write("Here is the contract, sign it by typing 'sign' + <your-name>!") #TODO: update the contract
            return

        self._engine.reset(hard=True) # reload new game but keeping player's names

    def write(self, mess: str) -> None:
        self.query_one(RichLog).write(mess)

    def clear(self):
        self.query_one(RichLog).clear()

    def key_enter(self) -> None:
        self.query_one(CmdsInput).focus()

    def key_escape(self) -> None:
        self.set_focus(None)

    @on(CmdsInput.Submitted)
    def _cmds_handler(self, event: CmdsInput.Submitted):
        event.inputer.value = ""

# ---Main App---
class BuckshotApp(App): 
    ENABLE_COMMAND_PALETTE = False
    TITLE = "BUCKSHOTxROULETTE"

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
        self.engine = BuckshotEngine()
        self.players: list[str] = []
        super().__init__()

    @property
    def version(self):
        try: 
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"

    def compose(self) -> ComposeResult:
        return super().compose()

    def on_mount(self):
        pass
