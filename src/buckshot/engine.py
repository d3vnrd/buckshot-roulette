from __future__ import annotations
from .entity import *
from .action import *

class BuckshotEngine:
    _valid_actions: dict[str, type[Action]] = {
        "magnifier": UseMagnifierAction,
        "beer": UseBeerAction,
        "handsaw": UseHandsawAction,
        "cigarette": UseCigaretteAction,
        "handcuff": UseHandcuffAction,
        "gun": UseGunAction
    }

    _stage: int = 0
    _turn: int = 0
    _health_cap: int = 3 # I: 3, II: 4, III: 5
    _items_per_reload: int = 2 # I: 2, II: 4, III: 4
    _observers: list[BuckshotObserver] = []

    _shotgun: Shotgun = Shotgun()
    _players : tuple[Player, ...]

    @dataclass(frozen=True)
    class BuckshotState:
        message: str
        stage: int
        turn: int
        players: tuple[Player.PlayerState, ...]
        shotgun: Shotgun.ShotgunState
        winner: Player|None

    class BuckshotObserver:
        @abstractmethod
        def on_engine_update(
            self, 
            state: BuckshotEngine.BuckshotState
        ) -> None:
            pass

    def __init__(self, p1_name: str, p2_name: str) -> None:
        self._players = (
            Player(p1_name, self._health_cap),
            Player(p2_name, self._health_cap)
            if p2_name else Dealer(self._health_cap)
        )

    """Observer + Mediator = Transmitter"""
    def attach(self, observer: BuckshotObserver) -> None:
        self._observers.append(observer)

    def _notify(self, message: str = "") -> None:
        for observer in self._observers:
            observer.on_engine_update(
                self.BuckshotState(
                    message = message,
                    stage = self._stage,
                    turn = self._turn,
                    players = tuple(p.state for p in self._players),
                    shotgun = self._shotgun.state,
                    winner = self._get_winner()
                )
            )

    """Business Logic Goes Here"""
    def _get_roles(self):
        return (
            self._players[self._turn],
            self._players[1 - self._turn]
        )

    def _get_winner(self):
        return next((
            p for p in self._players 
            if p.health > 0
        ), None)

    def _next_player(self):
        _, target = self._get_roles()
        if target.turn:
            self._turn = 1 - self._turn
        target.turn = True

    def _next_stage(self):
        self._health_cap += 1 if self._health_cap <= 5 else 0
        self._items_per_reload = 4
        self._stage += 1

    def reset(self, hard: bool = False):
        self._shotgun.reload()
        for player in self._players:
            if hard:
                player.reset(self._health_cap)
            player.inventory.add_items(self._items_per_reload)

        self._notify()

    def execute(self, args: list[str]):
        cmd = args[0]
        if cmd not in self._valid_actions:
            return

        actor, target = self._get_roles()
        if len(args) > 1 and args[1] == "self":
            target = actor

        result = self._valid_actions[cmd](actor, target).execute()
        if result.end_turn:
            self._next_player()

        self._notify(result.response)
