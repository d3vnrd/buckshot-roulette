from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass

from .entity import Coordinator, Dealer, Player, Shotgun
from .state import FSM, GameOverState, InitState
from .util import MsgType

class BuckshotEngine:
    @dataclass(frozen=True)
    class State:
        response: str
        stage: str
        n_items: int
        players: tuple[Player.PlayerState, ...]
        shotgun: Shotgun.ShotgunState
        winner: Player
        exit: bool

    class Observer:
        @abstractmethod
        def on_engine_update(
            self, 
            state: BuckshotEngine.State
        ) -> None:
            pass

    _observers: list[BuckshotEngine.Observer] 
    _state: FSM
    _coordinator: Coordinator
    _players : dict[str, Player]

    STAGE: int = 1
    MAX_HEALTH: int = 3 # I: 3, II: 4, >= III: 5
    N_ITEMS: int = 2 # I: 2, II: 4, >= III: 4
    WINNER: Player|None = None

    ACTOR: Player
    TARGET: Player
    SHOTGUN: Shotgun

    def __init__(self) -> None:
        self._observers = []
        self._state = InitState()
        self._players = {}

    """Observer + Mediator = Transmitter"""
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def notify(self, response: str = "", type: MsgType = "") -> None:
        for observer in self._observers:
            pass

    """Business Logic Goes Here"""
    @property
    def ready(self) -> bool:
        """Engine is ready when there are at least 1 player signs the contract"""
        return len(self._players) >= 2

    @property
    def can_continue(self) -> bool:
        """Able to continue to the next stage"""
        return all([
            self.ready,
            type(self.WINNER) is Player, # not None nor Dealer
            type(self._state) is GameOverState
        ])

    @property
    def is_player_turn(self) -> bool:
        return type(self.ACTOR) is Player

    def assign(self, name: str) -> None:
        if not name:
            return

        name = name.upper()

        if name in ["DEALER", "GOD"]:
            raise Exception(f"Invalid name: {name}")

        if name in self._players:
            raise Exception(f"{name} already existed")

        if len(self._players) > 2: # to-remove in the future
            raise Exception("Current Game state only supports 1v1 ...")

        self._players[name] = Player(name, self.MAX_HEALTH)

    def resign(self, name: str) -> None:
        if not name:
            return

        name = name.upper()

        player = self._players.pop(name, None)
        if not player:
            raise Exception(f"Player '{name}' not found")

    def start(self) -> None:
        """Create coordinator and start the game"""
        if not self.ready:
            # add Dealer when there is only 1 player
            self._players["Dealer"] = Dealer(self.MAX_HEALTH)

        self._coordinator = Coordinator(self._players)
        self.SHOTGUN = Shotgun()
        self.reset()

    def reset(self, hard: bool = False) -> None:
        """Add new items, reload shotgun, & optional hard reset players"""
        if not self.ready:
            raise Exception("Reset required engine to be ready")

        if hard:
            map(lambda p: p.reset(self.MAX_HEALTH), self._players.values())
            self._coordinator = Coordinator(self._players)
            self.STAGE = 1
            self.N_ITEMS = 2
            self.MAX_HEALTH = 3
            self.WINNER = None

        self.SHOTGUN.reload()
        map(lambda p: p.inventory.add(self.N_ITEMS), self._players.values()) # this still point to the same players in the queue

    def next_player(self):
        """Process to next player turn"""
        try:
            self.ACTOR = next(self._coordinator)
        except StopIteration:
            raise Exception("Coordinator is empty")

    def next_stage(self):
        """Process to next stage"""
        self._coordinator = Coordinator(self._players)
        self.WINNER = None
        self.STAGE += 1
        self.N_ITEMS += 2 if self.N_ITEMS < 4 else 0
        self.MAX_HEALTH += 1 if self.MAX_HEALTH < 5 else 0

    def execute(self, item: str = "", target: str = "") -> None:
        """
        Process player action, i.e. Use Item

        Expected behavior:
        - Raise error when not in AwaitActionState
        - Self state advance with While loop of coordinator is not empty
        """
        self.TARGET = self._players.get(target, self.TARGET)

        while self._coordinator: # execute when this is not empty (handled by __bool__)
            try:
                new_state = self._state.update(self, item)
                if new_state is self._state:
                    break

                self._state.on_exit(self)
                self._state = new_state
                self._state.on_enter(self)
            except Exception as e:
                # handle errors in internal state
                raise Exception(str(e))
        else:
            self.WINNER = self.ACTOR
