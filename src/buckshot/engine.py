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

    _curr_idx: int = 0
    _observers: list[BuckshotObserver] = []

    _stage: Stage = Stage()
    _shotgun: Shotgun = Shotgun()
    _players : tuple[Player, Player]

    @dataclass
    class BuckshotState:
        players: tuple[Player.PlayerState, ...]
        shotgun: Shotgun.ShotgunState
        stage: Stage
        message: str = ""
        winner: Player|None = None
        curr_turn_idx: int = 0
        game_over: bool = False

    class BuckshotObserver:
        @abstractmethod
        def on_engine_update(
            self, 
            state: BuckshotEngine.BuckshotState
        ) -> None:
            pass

    @property
    def state(self) -> BuckshotState:
        return self.BuckshotState(
            players = tuple(map(lambda player: player.state, self._players)),
            shotgun=self._shotgun.state,
            stage = self._stage,
        )

    """Observer + Mediator = Transmitter"""
    def attach(self, observer: BuckshotObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: BuckshotObserver) -> None:
        self._observers.remove(observer)

    def _notify(self) -> None:
        for observer in self._observers:
            observer.on_engine_update(self.state)

    """Business Logic Goes Here"""
    def _get_roles(self):
        return (
            self._players[self._curr_idx],
            self._players[1 - self._curr_idx]
        )

    def _next_player(self):
        _, target = self._get_roles()

        if not target.turn:
            target.turn = True
        else:
            self._curr_idx = 1 - self._curr_idx

    def _reset(self):
        self._shotgun.reload(4)
        for player in self._players:
            player.reset(self._stage.health_cap)

    def _action_execute(self):
        pass

    def setup(self, p01name:str, p02name:str):
        self._players = (
            Player(p01name, self._stage.health_cap),
            Player(p02name, self._stage.health_cap)
            if p02name else Dealer(self._stage.health_cap)
        )

        self._notify()
