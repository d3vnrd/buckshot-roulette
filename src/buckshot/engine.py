from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable, TYPE_CHECKING

from buckshot.entity import Dealer
from buckshot.state import InitState

if TYPE_CHECKING:
    from buckshot.state import FSM
    from buckshot.entity import Player, Shotgun

class BuckshotEngine:
    @dataclass(frozen=True)
    class State:
        response: str
        stage: str
        turn: int
        n_items: int
        players: tuple[Player.PlayerState, ...]
        shotgun: Shotgun.ShotgunState
        winner: Player|None

    @dataclass(frozen=True)
    class Command:
        handler: Callable
        turn_req: bool = False
        board_req: bool = False
        n_args: int = 0
        once: bool = False
        description: str = ""

    @dataclass(frozen=True)
    class Trigger:
        item: str
        target_id: int | None = None

    class Observer:
        @abstractmethod
        def on_engine_update(
            self, 
            state: BuckshotEngine.State
        ) -> None:
            pass

    _observers: list[Observer]
    _state: FSM

    STAGE: int = 1
    TURN: int = 0
    MAX_HEALTH: int = 3 # I: 3, II: 4, III: 5
    N_ITEMS: int = 2 # I: 2, II: 4, III: 4

    PLAYERS : list[Player]
    ACTOR: Player
    TARGET: Player
    SHOTGUN: Shotgun

    def __init__(self) -> None:
        self._observers = []
        self._state = InitState()
        self.PLAYERS = []

    @property
    def ready(self):
        return True if hasattr(self, "PLAYERS") else False

    """Observer + Mediator = Transmitter"""
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self, response: str = "") -> None:
        for observer in self._observers:
            pass

    """Business Logic Goes Here"""
    def assign(self, name: str):
        """Add new player to PLAYERS list"""
        self.PLAYERS.append(
            Player(name, self.MAX_HEALTH)
            if name else Dealer(self.MAX_HEALTH)
        )

    def next_player(self):
        """Process to next player turn"""
        pass

    def next_stage(self):
        """Process to next stage"""
        pass

    def execute(self, *args: str) -> None:
        """handle player intent and transfer it into Trigger"""
        pass
