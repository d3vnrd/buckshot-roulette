from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from buckshot.action import *
from buckshot.entity import *
if TYPE_CHECKING:
    from buckshot.engine import BuckshotEngine

class FSM(ABC):
    @abstractmethod
    def update(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger | None) -> FSM:
        pass

    def on_enter(self, engine: BuckshotEngine) -> None:
        pass

    def on_exit(self, engine: BuckshotEngine) -> None:
        pass

class InitState(FSM):
    def update(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger | None) -> FSM:
        if not engine.ready:
            return self

        engine.SHOTGUN = Shotgun()
        return AwaitActionState()

    def on_exit(self, engine: BuckshotEngine) -> None:
        engine.notify("Good, you sign the contract. NOW, let's us begin!", type="done")

class AwaitActionState(FSM):
    def on_enter(self, engine: BuckshotEngine) -> None:
        if engine.SHOTGUN.is_empty:
            engine.reset()

    def update(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger | None) -> FSM:
        if trigger is None:
            return self

        if trigger.item not in VALID_ACTIONS:
            engine.notify("Invalid item use.", type="error")
            return self

        action = VALID_ACTIONS[trigger.item](engine)
        return ResolveActionState(action)

class ResolveActionState(FSM):
    class EndTurnState(FSM):
        def update(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger | None) -> FSM:
            engine.next_player()
            return AwaitActionState()

    class GameOverState(FSM):
        def update(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger | None) -> FSM:
            return self

    def __init__(self, action: Action) -> None:
        self.action = action

    def update(self, engine: BuckshotEngine, trigger: BuckshotEngine.Trigger | None) -> FSM:
        result = self.action.execute()

        if result.game_over:
            return self.GameOverState()

        if result.end_turn:
            return self.EndTurnState()

        return AwaitActionState()

