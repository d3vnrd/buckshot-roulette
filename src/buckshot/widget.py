from __future__ import annotations
from typing import Literal, Self, override

from textual import on
from textual.app import ComposeResult
from textual.containers import Container, HorizontalGroup
from textual.message import Message
from textual.reactive import reactive
from textual.suggester import Suggester
from textual.widget import Widget
from textual.widgets import (
    Input,
    Label,
    RichLog,
    Static,
)
from buckshot.engine import BuckshotEngine

# --- Buckshot Game Container ---
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

class BoardView(Container):
    DEFAULT_CSS = """
    BoardView {
        width: 1fr;
        height: 1fr;
        border: round white;
        border-subtitle-align: center;
        margin: 1 2 0 2;
        layout: grid;
        grid-size: 2 2;
        grid-rows: 1fr auto;
    }

    BoardView .sub-panel {
        width: 1fr;
        align: center top;
        border-top: solid white;
        border-title-align: center;
        padding: 1 2 0 2;
    }

    BoardView Static {
        width: 1fr;
        height: 1;
    }

    BoardView .right-align {
        content-align: right middle;
    }
    """
    BORDER_SUBTITLE = ">_"

# --- Custom widgets ---
class Logs(RichLog, BuckshotEngine.Observer):
    MessageType = Literal["", "info", "warn", "error", "success"]
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

    def __init__(self, engine: BuckshotEngine) -> None:
        super().__init__(wrap=True, markup=True)
        engine.attach(self)

    @override
    def write(self, mess: str, type: MessageType = "", *arg, **kwargs) -> Self:
        output = ""
        match type:
            case "error":
                output = "[bold red]Error: " + mess
            case "success":
                output = "[bold green]Done: " + mess
            case _:
                output = mess

        return super().write(output)

    @override
    def on_engine_update(self, state: BuckshotEngine.State):
        self.write(f"Player executed a command: {state.response}", type="success")

class StatsReport(Widget, BuckshotEngine.Observer):
    BORDER_TITLE = " 󰷨 Board's Status "
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

    def __init__(self, engine: BuckshotEngine) -> None:
        super().__init__(classes="sub-panel")
        engine.attach(self)
        self.display = False

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

    @override
    def on_engine_update(self, state: BuckshotEngine.State):
        self.display = not False
        self.chamber = " ".join(["󰲅"] * state.shotgun.bullets_left)
        self.turn = state.players[state.turn].name.upper()
        self.items = str(state.n_items)
        self.stage = state.stage

class PlayerInfo(Widget, BuckshotEngine.Observer):
    BORDER_TITLE = "  Player's Info "
    ICONS = {
        "magnifier": "󰍉", 
        "beer": "󱄖", 
        "cigarette": "󱆉", 
        "handsaw": "󰹈", 
        "handcuff": "󱄾",
    }

    DEFAULT_CSS = """
    PlayerInfo {
        height: auto;
        width: 1fr;
        padding-bottom: 1;
    }

    PlayerInfo Label {
        width: auto;
        padding-right: 1;
    }

    PlayerInfo HorizontalGroup {
        margin-bottom: 1;
    }
    """

    pname: reactive[str] = reactive("")
    health: reactive[str] = reactive("")
    inventory: reactive[str] = reactive("")

    def __init__(self, engine: BuckshotEngine) -> None:
        super().__init__(classes="sub-panel")
        engine.attach(self)
        self.display = False

    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Label(f"{self.pname}:", id="player-pname")
            yield Static(self.health, id="player-health")
        yield Static(self.inventory, id="player-inventory")

    def on_mount(self):
        def w_func(attr: str):
            return lambda v: self.query_one(f"#player-{attr}", Static).update(v)

        for attr in ["pname", "health", "inventory"]:
            self.watch(self, attr, w_func(attr))

    @override
    def on_engine_update(self, state: BuckshotEngine.State):
        self.display = not False
        p_state = state.players[0]
        self.pname = p_state.name.upper() + ":"
        self.health = " ".join(["󱐋" * p_state.health])
        self.inventory = " | ".join(f"{self.ICONS[k]} {v}" for k, v in p_state.inventory.items())

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

    def __init__(self, suggester: Suggester) -> None:
        self.suggester = suggester
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Static(">")
        yield Input(suggester=self.suggester, placeholder="Enter commands ...", compact=True)

    @on(Input.Submitted)
    def parse(self, event: Input.Submitted) -> None:
        if not event.value.strip():
            return

        cmd = event.value.lower().strip().split()
        action, args = cmd[0], cmd[1:]
        self.post_message(self.Submitted(event.input, action, args))
