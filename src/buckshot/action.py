from __future__ import annotations
from typing import TYPE_CHECKING, override
from dataclasses import dataclass
from abc import ABC, abstractmethod

from .util import *

if TYPE_CHECKING:
    from .engine import BuckshotEngine
    from .entity import Player, Shotgun

@dataclass(frozen=True)
class ActionResult:
    response: str = ""
    end_turn: bool = True
    skip_turn: bool = False

class Action(ABC):
    def __init__(self, engine: BuckshotEngine):
        self.ACTOR: Player = engine.ACTOR
        self.TARGET: Player = engine.TARGET
        self.SHOTGUN: Shotgun = engine.SHOTGUN

    @abstractmethod
    def execute(self) -> ActionResult:
        pass

# Failed cases: 
# - Empty chamber (should never happen)
class UseGunAction(Action):
    @override
    def execute(self):
        shell = self.SHOTGUN.eject()
        self_target = self.TARGET is self.ACTOR

        if shell is None:
            raise EmptyChamberError

        if shell is False and self_target:
            return ActionResult(
                response="Blank shell, skip next player's turn", 
                skip_turn=True
            )

        self.SHOTGUN.damage = 1
        dmg = self.SHOTGUN.damage
        self.TARGET.health -= dmg
        return ActionResult(
            response=f"LIVE shell, {self.ACTOR.name} deals {dmg} to {"themself" if self_target else self.TARGET.name}", 
        )


# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseMagnifierAction(Action):
    @override
    def execute(self):
        return ActionResult(response="Use Magnifier")

# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseBeerAction(Action):
    @override
    def execute(self):
        return ActionResult(response="Use Beer")

# Failed cases: 
# - Does not have item
class UseHandsawAction(Action):
    @override
    def execute(self):
        return ActionResult()

# Failed cases: 
# - Does not have item
# - User is at full health
class UseCigaretteAction(Action):
    @override
    def execute(self):
        return ActionResult()

# Failed cases:
# - Does not have item
# - Current target turn has been skipped (use more than 1 handcuff)
class UseHandcuffAction(Action):
    @override
    def execute(self):
        return ActionResult()

VALID_ACTIONS: dict[str, type[Action]] = {
    "magnifier": UseMagnifierAction,
    "beer": UseBeerAction,
    "handsaw": UseHandsawAction,
    "cigarette": UseCigaretteAction,
    "handcuff": UseHandcuffAction,
    "gun": UseGunAction
}
