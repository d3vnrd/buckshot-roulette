from __future__ import annotations
from typing import TYPE_CHECKING, Callable, override
from dataclasses import dataclass
from abc import ABC, abstractmethod

from buckshot.entity import Player, Shotgun

if TYPE_CHECKING:
    from buckshot.engine import BuckshotEngine

@dataclass
class Command:
    handler: Callable
    turn_req: bool = False
    board_req: bool = False
    n_args: int = 0
    once: bool = False
    description: str = ""

@dataclass
class ActionResult:
    response: str = ""
    end_turn: bool = True
    skip_turn: bool = False
    game_over: bool = False

class Action(ABC):
    ACTOR: Player
    TARGET: Player
    SHOTGUN: Shotgun

    def __init__(self, engine: BuckshotEngine):
        self.ACTOR = engine.ACTOR
        self.TARGET = engine.TARGET
        self.SHOTGUN = engine.SHOTGUN

    @abstractmethod
    def execute(self) -> ActionResult:
        pass

# Failed cases: 
# - Empty chamber (should never happen)
class UseGunAction(Action):
    @override
    def execute(self):
        shell = self.SHOTGUN.eject()
        skip_turn = False

        if shell is None:
            pass

        if shell is True:
            self.TARGET.health -= self.SHOTGUN.damage

        if shell is False and self.TARGET is self.ACTOR:
            skip_turn = True

        self.SHOTGUN.damage = 1
        return ActionResult(response="Use Gun", skip_turn=skip_turn)

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
