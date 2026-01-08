from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from buckshot.action import VALID_ACTIONS

if TYPE_CHECKING:
    from .engine import BuckshotEngine
    from .entity import Player
    from .action import Action

class FSM(ABC):
    @abstractmethod
    def update(self, engine: BuckshotEngine, input: str) -> FSM:
        """Process input and return next state (REQUIRED)"""
        pass
    
    def on_enter(self, engine: BuckshotEngine) -> None:
        """Called when entering this state (OPTIONAL)"""
        pass
    
    def on_exit(self, engine: BuckshotEngine) -> None:
        """Called when exiting this state (OPTIONAL)"""
        pass

class InitState(FSM):
    def update(self, engine: BuckshotEngine, input: str = "") -> FSM:
        return AwaitActionState()

class AwaitActionState(FSM):
    _prev: Player
    _instance: FSM|None = None

    def on_enter(self, engine: BuckshotEngine) -> None:
        """Ensure that SHOTGUN is not empty before any action"""
        if engine.SHOTGUN.is_empty:
            engine.reset()

        if engine.ACTOR is not self._prev:
            engine.notify(f"Begin {engine.ACTOR.name}'s turn ...'")
            self._prev = engine.ACTOR

    def update(self, engine: BuckshotEngine, input: str = "") -> FSM:
        if not input:
            return self

        if input not in VALID_ACTIONS:
            raise Exception("Invalid item use")

        action = VALID_ACTIONS[input](engine)
        return ResolveActionState(action)

    def __new__(cls):
        """Singleton ensure this class is only create once and use everywhere else"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

class ResolveActionState(FSM):
    def __init__(self, action: Action) -> None:
        self.result = action.execute()

    def update(self, engine: BuckshotEngine, input: str = "") -> FSM:
        engine.notify(self.result.response, type="done")

        if self.result.end_turn:
            engine.notify(f"{engine.ACTOR.name}'s turn end. Continuing ...'", type="done")
            engine.next_player()

        return AwaitActionState()

class GameOverState(FSM):
    def update(self, engine: BuckshotEngine, input: str = "") -> FSM:
        if engine.WINNER is None:
            return AwaitActionState()
        return self
