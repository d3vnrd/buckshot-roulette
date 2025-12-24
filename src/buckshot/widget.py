from __future__ import annotations
from typing import override

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import (
    Input,
    Label,
    RichLog,
    Static,
)
from buckshot.engine import BuckshotEngine

class GameContainer(Container):
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

    def __init__(self) -> None:
        super().__init__()
        self.border_title = f"󰍉 󱄾 {self.app.title} 󱆉 󰹈"
        self.border_subtitle = f"v{self.app.sub_title}"

class BoardView(Container, BuckshotEngine.BuckshotObserver):
    DEFAULT_CSS = """
    BoardView {
        width: 1fr;
        height: 1fr;
        border: round white;
        border-subtitle-align: center;
        margin: 0 1 0 1;
        layout: grid;
        grid-size: 2;
        grid-rows: 1fr auto;
    }
    """

    class Logs(RichLog):
        DEFAULT_CSS = """
        Logs {
            background: $background;
            margin: 0 1 0 1;
            column-span: 2;
        }

        Logs:focus {
            background: rgba(0, 0, 0, 0);
        }
        """
        def __init__(self) -> None:
            super().__init__(wrap=True, markup=True)

        def update(self, state: BuckshotEngine.BuckshotState):
            self.write(state.message)

    class StatsReport(Widget):
        BORDER_TITLE = " 󰷨 Board's Status "
        DEFAULT_CSS = """
        StatsReport {
            width: 1fr;
            align: center top;
            border-top: solid white;
            border-title-align: center;
            padding: 1 2 0 2;
        }

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
        DEFAULT_CSS = """
        PlayerInfo {
            width: 1fr;
            align: center top;
            border-top: solid white;
            border-title-align: center;
            padding: 1 2 0 2;
        }
        """

        def compose(self) -> ComposeResult:
            yield Static("[dim]Nothing to show yet![/dim]")

        def update(self, state: BuckshotEngine.BuckshotState):
            self.query_one(Static).update("Something to show!")

    def __init__(self, engine: BuckshotEngine) -> None:
        super().__init__()
        self.border_subtitle = ">_"
        engine.attach(self)

    def compose(self) -> ComposeResult:
        yield self.Logs()
        yield self.StatsReport()
        yield self.PlayerInfo()

    def write(self, mess: str, type: str = ""):
        log = self.query_one(self.Logs)

        match type:
            case "error":
                log.write("[bold magenta]" + mess)
            case _:
                log.write(mess)

    def clear(self):
        self.query_one(self.Logs).clear()

    def on_mount(self):
        pass

    @override
    def on_engine_update(self, state: BuckshotEngine.BuckshotState) -> None:
        pass

# --- Custom widgets ---
class PlayerInput(Widget):
    DEFAULT_CSS = """
    PlayerInput {
        layout: horizontal;
        width: 1fr;
        height: 3;
        align: center middle;
        padding: 0 2 0 2;
    }

    PlayerInput Static {
        width: auto;
        height: 1;
    }

    PlayerInput Input {
        width: 1fr;
        height: 1;
        background: $background;
        margin-left: 1;
    }

    PlayerInput Input:focus {
        background: rgba(0, 0, 0, 0);
    }
    """

    class Submitted(Message):
        def __init__(self, input: Input,  action: str, args: list[str]) -> None:
            self.input = input
            self.action = action
            self.args = args
            super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(">")
        yield Input(
            placeholder="Enter commands ...", 
            compact=True,
        )

    @on(Input.Submitted)
    def parse(self, event: Input.Submitted) -> None:
        if not event.value.strip():
            return

        cmd = event.value.lower().strip().split()
        action, args = cmd[0], cmd[1:]
        self.post_message(self.Submitted(event.input, action, args))
