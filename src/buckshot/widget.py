from __future__ import annotations
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (
    Input,
    Label,
    RichLog,
    Static
)
from buckshot.engine import BuckshotEngine

class GameContainer(Widget):
    DEFAULT_CSS = """
    GameContainer {
        width: 80;
        height: 40;
        border: round white;
        border-title-align: center;
        border-subtitle-align: right;
        align: center middle;
    }
    """
    def __init__(self, *children: Widget) -> None:
        self.border_title = f"󰍉 󱄾 {self.app.title} 󱆉 󰹈"
        self.border_subtitle = f"v{self.app.sub_title}"
        super().__init__(*children)

class GameStatus(Widget, BuckshotEngine.BuckshotObserver):
    DEFAULT_CSS = """
    GameStatus {
        width: 1fr;
        height: 1fr;
        border: round white;
        margin: 0 1 0 1;
        layout: grid;
        grid-size: 2 2;
        grid-rows: 2fr auto;
    }

    GameStatus .sub-panel {
        width: 1fr;
        align: center top;
        border-top: solid white;
        border-title-align: center;
        padding: 1 2 0 2;
    }
    """

    class Logs(RichLog):
        DEFAULT_CSS = """
        Logs{
            background: $background;
            margin: 0 1 0 1;
            column-span: 2;
        }

        Logs:focus {
            background: rgba(0, 0, 0, 0);
        }
        """

        def update(self):
            pass

    class StatsReport(Widget):
        BORDER_TITLE = " 󰷨 Board's Status "
        DEFAULT_CLASSES = "sub-panel"
        DEFAULT_CSS = """
        StatsReport HorizontalGroup {
            height: 1;
            margin-bottom: 1;
            align: center middle;
        }
        """

        chamber: reactive[str] = reactive("?")
        turn: reactive[str] = reactive("?")
        items: reactive[str] = reactive("?")
        stage: reactive[str] = reactive("?")

        def compose(self) -> ComposeResult:
            for label, attr in [
                ("Bullets Left:", "chamber"),
                ("Current Turn:", "turn"),
                ("Items Add:", "items"),
                ("Stage:", "stage"),
            ]:
                with HorizontalGroup():
                    yield Label(label)
                    yield Static(getattr(self, attr), id=f"status-{attr}", classes="right-align")

        def on_mount(self) -> None:
            def w_func(attr: str):
                return lambda v: self.query_one(f"#status-{attr}", Static).update(v)

            for attr in ["chamber", "turn", "items", "stage"]:
                self.watch(self, attr, w_func(attr))

        def update(self, state: BuckshotEngine.BuckshotState):
            self.chamber = " ".join(["󰲅"] * state.shotgun.bullets_left)
            self.turn = state.players[state.turn].name
            self.items = str(state.items_per_reload)
            self.stage = state.stage

    class PlayerInfo(Widget):
        ICONS = {
            "magnifier": "󰍉", 
            "beer": "󱄖", 
            "cigarette": "󱆉", 
            "handsaw": "󰹈", 
            "handcuff": "󱄾",
        }

        BORDER_TITLE = "  Player's Info "
        DEFAULT_CLASSES = "sub-panel"

        def compose(self) -> ComposeResult:
            yield Static("[dim]Nothing to show yet![/dim]", id="placeholder")

        def update(self):
            pass

    def __init__(self, engine: BuckshotEngine) -> None:
        self.engine = engine
        super().__init__()
        engine.attach(self)

    def compose(self) -> ComposeResult:
        yield self.Logs()
        yield self.StatsReport()
        yield self.PlayerInfo()

    def on_mount(self):
        for w in self.query("StatsReport, PlayerInfo"):
            w.display = False

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState) -> None:
        for w in self.query("Logs, StatsReport, PlayerInfo"):
            w.update()

class CmdsInput(Widget, BuckshotEngine.BuckshotObserver):
    DEFAULT_CSS = """
    CmdsInput {
        layout: horizontal;
        width: 1fr;
        height: 3;
        align: center middle;
        padding: 0 2 0 2;
    }

    CmdsInput Input {
        background: $background;
        margin-left: 1;
    }

    CmdsInput Input:focus {
        background: rgba(0, 0, 0, 0);
    }
    """

    class Submitted(Message):
        def __init__(self, value: str, inputer: Input) -> None:
            self.value = value
            self.inputer = inputer
            super().__init__()

    def __init__(self, engine: BuckshotEngine) -> None:
        super().__init__()
        engine.attach(self)

    def compose(self) -> ComposeResult:
        yield Static(">")
        yield Input(placeholder="Enter commands ...", compact=True)

    def focus(self, scroll_visible: bool = True) -> Widget:
        return self.query_one(Input).focus()

    @on(Input.Submitted)
    def _send(self, event: Input.Submitted):
        self.post_message(self.Submitted(event.value, self.query_one(Input)))
