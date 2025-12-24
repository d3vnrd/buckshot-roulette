from __future__ import annotations
from importlib.metadata import PackageNotFoundError, version

from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.suggester import SuggestFromList

from buckshot.engine import BuckshotEngine
from buckshot.action import Command
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

    @property
    def version(self):
        try: 
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"

    @property
    def view(self):
        return self.query_one(BoardView)

    @property
    def commands(self) -> dict[str, Command]:
        return {
            "clear": Command(
                handler=self.view.clear,
                turn_req=True,
                description="Clear game logs"
            ),
            "exit": Command(
                handler=self.app.exit,
                turn_req=False,
                description="Exit the game"
            ),
            "help": Command(
                handler=self.action_show_help,
                turn_req=False,
                description="Show available commands"
            ),
            "reset": Command(
                handler=lambda: self.ENGINE.reset(hard=True),
                turn_req=False,
                description="Reset the current game"
            ),
            "use": Command(
                handler=self.ENGINE.execute,
                turn_req=True,
                n_args=1,
                description="Use an item"
            ),
            "sign": Command(
                handler=self.ENGINE.sign,
                once=True,
                n_args=1,
                description="Assign player and start the game",
            )
        }

    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with GameContainer():
                yield BoardView(self.ENGINE)
                yield PlayerInput()

    def action_show_help(self) -> None:
        pass

    def action_show_contract(self) -> None:
        pass

    def action_is_player_turn(self) -> bool:
        return self.ENGINE.ready and self.ENGINE._turn == 0

    def key_enter(self):
        self.query_one("PlayerInput Input").focus()

    def on_mount(self):
        self.query_one("PlayerInput Input", Input).suggester = SuggestFromList(self.commands)

    @on(PlayerInput.Submitted)
    def execute(self, event: PlayerInput.Submitted) -> None:
        """
        Behavior:
        - Reset Input value on success command executed (notify player that their input is invalid)
        - Recieve event message from PlayerInput and execute based on action and args given.
        - Report any issues with command executions.
        """
        cmd = self.commands.get(event.action)

        if cmd is None:
            return

        if cmd.turn_req and not self.action_is_player_turn():
            return

        if cmd.once and self.ENGINE.ready:
            return

        if event.args:
            if len(event.args) != cmd.n_args:
                return
            else:
                cmd.handler(*event.args)
        else:
            cmd.handler()

        event.input.value = "" # reset value on success
