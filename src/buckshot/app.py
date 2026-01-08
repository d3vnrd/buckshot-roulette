from __future__ import annotations
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from typing import Callable

from textual import on
from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.suggester import SuggestFromList

from .engine import BuckshotEngine
from .util import MsgType
from .widget import *

class BuckshotApp(App): 
    ENABLE_COMMAND_PALETTE = False
    TITLE = "BUCKSHOTxROULETTE"
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

    @dataclass(frozen=True)
    class Command:
        handler: Callable
        n_args: int = 0
        once: bool = False
        conds: bool = True
        description: str = ""

    _engine: BuckshotEngine
    _cmds_history: list[Command]

    def __init__(self):
        super().__init__()
        self.sub_title = self.version
        self._engine = BuckshotEngine()
        self._cmds_history = []

    """Textual App Funcitons"""
    def compose(self) -> ComposeResult:
        with ScrollableContainer():
            with GameContainer():
                with BoardView():
                    yield from (w(self._engine) for w in [
                        Logs, StatsReport, PlayerInfo
                    ])
                yield PlayerInput(SuggestFromList([]))

    def key_enter(self):
        self.query_one("PlayerInput Input").focus()

    """Buckshot Helper Functions"""
    @property
    def version(self):
        try: 
            return version("buckshot-roulette")
        except PackageNotFoundError:
            return "Unknown"

    @property
    def commands(self) -> dict[str, Command]:
        return {
            "clear": self.Command(
                handler=self.clear,
                description="Clear game logs",
            ),
            "continue": self.Command(
                handler=self._engine.execute,
                conds=self._engine.can_continue,
                description="Process to the next stage",
            ),
            "exit": self.Command(
                handler=self.app.exit,
                description="Exit the game",
            ),
            "help": self.Command(
                handler=self.help,
                conds=self._engine.is_player_turn,
                description="Show available commands",
            ),
            "remove": self.Command(
                handler=self._engine.resign,
                n_args=1,
                conds=True, # TODO: What is the terminate condition for this cmd
                description="Resign a player",
            ),
            "restart": self.Command(
                handler=lambda: self._engine.reset(hard=True),
                description="Restart the current game",
            ),
            "start": self.Command(
                handler=self._engine.start,
                once=True,
                description="Start the game",
            ),
            "sign": self.Command(
                handler=self._engine.assign,
                n_args=1,
                description="Assign player",
            ),
            "use": self.Command(
                handler=self._engine.execute,
                n_args=1,
                conds=self._engine.is_player_turn,
                description="Use an item on the board",
            ),
        }

    @property
    def _logger(self) -> Logs:
        return self.query_one(Logs)

    def clear(self) -> None:
        self._logger.clear()

    def write(self, mess: str, type: MsgType = "") -> None:
        self._logger.write(mess, type)

    def help(self) -> None:
        pass

    @on(PlayerInput.Submitted)
    def execute(self, event: PlayerInput.Submitted) -> None:
        """
        Behavior:
        - Reset Input value on success command executed (notify player that their input is invalid)
        - Recieve event message from PlayerInput and execute based on action and args given.
        - Report any issues with command executions.
        - Disable on certain conditions
        """
        cmd = self.commands.get(event.action)

        if not cmd:
            self.write(f"Unknown {event.action}", type="error")
            return

        if any([
            not cmd.conds,
            (cmd.once and cmd in self._cmds_history),
        ]):
            self.write(f"<{event.action}> is currently disabled", type="error")
            return

        if len(event.args) != cmd.n_args:
            self.write("Invalid required arguments", type="error")
            return

        try:
            if event.args:
                cmd.handler(event.args)
            else:
                cmd.handler()

            self._cmds_history.append(cmd) # add cmd to history on success
            event.input.value = "" # reset value on success
        except Exception as e:
            self.write(str(e), type="error")
