from __future__ import annotations
from typing import TYPE_CHECKING, override
from dataclasses import dataclass
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from buckshot.engine import BuckshotEngine

class Action(ABC):
    @dataclass
    class ActionResult:
        end_turn: bool = True
        game_over: bool = False
        skip_turn: bool = False
        response: str = ""

    def __init__(self, engine: BuckshotEngine|None = None):
        self._engine = engine

    @property
    def mediator(self) -> BuckshotEngine|None:
        return self._engine

    @mediator.setter
    def mediator(self, engine: BuckshotEngine) -> None:
        self._engine = engine

    @abstractmethod
    def execute(self) -> ActionResult:
        pass

# Failed cases: 
# - Empty chamber (should never happen)
class UseGunAction(Action):
    @override
    def execute(self):
        return self.ActionResult()

# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseMagnifierAction(Action):
    @override
    def execute(self):
        return self.ActionResult()

# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseBeerAction(Action):
    @override
    def execute(self):
        return self.ActionResult()

# Failed cases: 
# - Does not have item
class UseHandsawAction(Action):
    @override
    def execute(self):
        return self.ActionResult()

# Failed cases: 
# - Does not have item
# - User is at full health
class UseCigaretteAction(Action):
    @override
    def execute(self):
        return self.ActionResult()

# Failed cases:
# - Does not have item
# - Current target turn has been skipped (use more than 1 handcuff)
class UseHandcuffAction(Action):
    @override
    def execute(self):
        return self.ActionResult()
