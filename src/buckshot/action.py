from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, override
from buckshot.error import (
    EmptyChamberError,
    InsufficientItemsError,
    InvalidActionError
)

if TYPE_CHECKING: 
    from buckshot.entity import Player, Shotgun, Stage

@dataclass
class ActionResult:
    """Result after a sucessful Action"""
    end_turn: bool = True
    game_over: bool = False
    skip_turn: bool = False
    response: str = ""

class Action(ABC):
    def __init__(
        self, 
        actor: Player, 
        target: Player, 
        shotgun: Shotgun, 
        stage: Stage
    ):
        self.actor: Player = actor
        self.target: Player = target
        self.shotgun: Shotgun = shotgun
        self.stage: Stage = stage

    @abstractmethod
    def execute(self) -> ActionResult:
        pass

# Failed cases: 
# - Empty chamber (should never happen)
class UseGunAction(Action):
    @override
    def execute(self):
        shell = self.shotgun.eject()
        game_over = False
        skip_turn = False

        if shell is None:
            raise EmptyChamberError()

        if shell is True:
            self.target.health -= self.shotgun.damage
            game_over = self.target.health <= 0

        if shell is False and self.target is self.actor:
            skip_turn = True

        self.shotgun.damage = 1
        return ActionResult(skip_turn=skip_turn, game_over=game_over)

class ItemAction(Action, ABC):
    def _consume_item(self, item: str):
        if not self.actor.inventory.has_item(item):
            raise InsufficientItemsError(item)
        self.actor.inventory.items[item] -= 1

# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseMagnifierAction(ItemAction):
    @override
    def execute(self):
        shell = self.shotgun.peek()
        if shell is None:
            raise EmptyChamberError()

        self._consume_item("magnifier")
        response = f"Current shell is {"Live" if shell else "Blank"}"
        return ActionResult(end_turn=False, response=response)

# Failed cases: 
# - Empty chamber (should never happen)
# - Does not have item
class UseBeerAction(ItemAction):
    @override
    def execute(self):
        shell = self.shotgun.eject()
        if shell is None:
            raise EmptyChamberError()

        self._consume_item("beer")
        response = f"Current ejected shell is {"Live" if shell else "Blank"}"
        return ActionResult(end_turn=False, response=response)

# Failed cases: 
# - Does not have item
class UseHandsawAction(ItemAction):
    @override
    def execute(self):
        self._consume_item("handsaw")
        self.shotgun.cutoff()
        return ActionResult(
            end_turn=False, 
            response=f"Doubled shotgun damage, current damage is: {self.shotgun.damage}."
        )

# Failed cases: 
# - Does not have item
# - User is at full health
class UseCigaretteAction(ItemAction):
    @override
    def execute(self):
        if self.actor.health >= self.stage.health_cap:
            raise InvalidActionError("Already at full health")

        self._consume_item("cigarette")
        self.actor.health += 1
        return ActionResult(end_turn=False, response="Healed 1 health.")

# Failed cases:
# - Does not have item
# - Current target turn has been skipped (use more than 1 handcuff)
class UseHandcuffAction(ItemAction):
    @override
    def execute(self):
        if not self.target.turn:
            raise InvalidActionError("Target's turn already skipped")

        self._consume_item("handcuff")
        self.target.turn = False
        return ActionResult(end_turn=False, response="Target's next turn will be skipped")
