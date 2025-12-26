from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from buckshot.action import *
from buckshot.entity import *
if TYPE_CHECKING:
    from buckshot.engine import BuckshotEngine

class FSM(ABC):
    @abstractmethod
    def handle(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger) -> FSM | None:
        pass

class InitState(FSM):
    def handle(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger) -> FSM | None:
        if not engine.ready:
            return self

        engine.SHOTGUN = Shotgun()
        return AwaitActionState()

class AwaitActionState(FSM):
    def handle(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger) -> FSM | None:
        if trigger.item not in VALID_ACTIONS:
            return self

        action = VALID_ACTIONS[trigger.item](engine)
        return ResolveActionState(action)

class ResolveActionState(FSM):
    class EndTurnState(FSM):
        def handle(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger) -> FSM | None:
            engine.next_player()

            if engine.SHOTGUN.is_empty:
                engine.SHOTGUN.reload()
                for p in engine.PLAYERS:
                    p.inventory.add(engine.N_ITEMS)

            return AwaitActionState()

    class GameOverState(FSM):
        def handle(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger) -> FSM | None:
            return self

    def __init__(self, action: Action) -> None:
        self.action = action

    def handle(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger) -> FSM | None:
        result = self.action.execute()

        if result.game_over:
            return self.GameOverState()

        if result.end_turn:
            return self.EndTurnState()

        return AwaitActionState()

