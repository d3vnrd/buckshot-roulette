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
    def commands(self) -> dict[str, Command]:
        return {
            "clear": Command(
                handler=self.query_one(Logs).clear,
                description="Clear game logs"
            ),
            "exit": Command(
                handler=self.app.exit,
                description="Exit the game"
            ),
            "help": Command(
                handler=self.help,
                description="Show available commands"
            ),
            "reset": Command(
                handler=lambda: self.ENGINE.reset(hard=True),
                turn_req=True,
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

    @property
    def is_player_turn(self) -> bool:
        return self.ENGINE.ready and self.ENGINE.TURN == 0

    @property
    def logger(self) -> Logs:
        return self.query_one(Logs)


    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with GameContainer():
                with BoardView():
                    yield from (w(self.ENGINE) for w in [
                        Logs, StatsReport, PlayerInfo
                    ])
                yield PlayerInput(SuggestFromList([]))

    def help(self) -> None:
        pass

    def key_enter(self):
        self.query_one("PlayerInput Input").focus()

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
            self.logger.write(f"Unknown {event.action}! Try <help> instead.", type="error")
            return

        #TODO: add other executed conditions for each commands

        if cmd.once and self.ENGINE.ready:
            return

        if event.args:
            if len(event.args) != cmd.n_args:
                self.logger.write("Invalid required arguments! Try <help> instead.", type="error")
                return
            else:
                cmd.handler(*event.args)
        else:
            cmd.handler()

        event.input.value = "" # reset value on success
