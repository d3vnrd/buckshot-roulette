from __future__ import annotations
from typing import override
from dataclasses import dataclass
from abc import ABC, abstractmethod

from buckshot.entity import Player

class Action(ABC):
    @dataclass
    class ActionResult:
        end_turn: bool = True
        skip_turn: bool = False
        response: str = ""

    def __init__(self, actor: Player, target: Player):
        self.actor = actor
        self.target = target

    @abstractmethod
    def execute(self) -> ActionResult:
        pass

# Failed cases: 
# - Empty chamber (should never happen)
class UseGunAction(Action):
    @override
    def execute(self):
        self.actor.inventory.add_items(1)
        return self.ActionResult(response="Use Gun")

# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseMagnifierAction(Action):
    @override
    def execute(self):
        return self.ActionResult(response="Use Magnifier")

# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseBeerAction(Action):
    @override
    def execute(self):
        return self.ActionResult(response="Use Beer")

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
