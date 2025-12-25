from __future__ import annotations
from .entity import *
from .action import *

class BuckshotEngine:
    @dataclass(frozen=True)
    class BuckshotState:
        response: str
        stage: str
        turn: int
        n_items: int
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

    _observers: list[BuckshotObserver]
    _actions: dict[str, type[Action]] = {
        "magnifier": UseMagnifierAction,
        "beer": UseBeerAction,
        "handsaw": UseHandsawAction,
        "cigarette": UseCigaretteAction,
        "handcuff": UseHandcuffAction,
        "gun": UseGunAction
    }

    STAGE: int = 1
    TURN: int = 0
    MAX_HEALTH: int = 3 # I: 3, II: 4, III: 5
    N_ITEMS: int = 2 # I: 2, II: 4, III: 4

    PLAYERS : tuple[Player, ...]
    ACTOR: Player
    TARGET: Player
    SHOTGUN: Shotgun

    def __init__(self) -> None:
        self._observers = []
        self.SHOTGUN = Shotgun()

    @property
    def ready(self):
        return True if hasattr(self, "PLAYERS") else False

    """Observer + Mediator = Transmitter"""
    def attach(self, observer: BuckshotObserver) -> None:
        self._observers.append(observer)

    def _notify(self, response: str = "") -> None:
        for observer in self._observers:
            observer.on_engine_update(
                self.BuckshotState(
                    response = response,
                    stage = {1: "I", 2: "II", 3: "III"}.get(self.STAGE, "?"),
                    turn = self.TURN,
                    n_items=self.N_ITEMS,
                    players = tuple(p.state for p in self.PLAYERS),
                    shotgun = self.SHOTGUN.state,
                    winner = self._get_winner()
                )
            )

    """Business Logic Goes Here"""
    def _get_winner(self):
        return next((
            p for p in self.PLAYERS 
            if p.health > 0
        ), None)

    def _next_player(self):
        pass

    def _next_stage(self):
        self.MAX_HEALTH += 1 if self.MAX_HEALTH <= 5 else 0
        self.N_ITEMS += 2 if self.N_ITEMS <= 4 else 0
        self.STAGE += 1

    def sign(self, name: str):
        self.PLAYERS = (
            Player(name, self.MAX_HEALTH),
            Dealer(self.MAX_HEALTH)
        )

    def reset(self, hard: bool = False):
        pass

    def execute(self, *args: str):
        item = args[0]
        if item not in self._actions:
            self._notify(f"Invalid {item} input!")
            return

        result = self._actions[item](self).execute()
        if result.end_turn:
            self._next_player()
            if self.SHOTGUN.is_empty:
                self.SHOTGUN.reload()
                for p in self.PLAYERS:
                    p.inventory.add_items(self.N_ITEMS)

        if result.game_over:
            self._get_winner()

        self._notify(result.response)
