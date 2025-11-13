from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from buckshot.entity import Player, Shotgun, Stage

@dataclass
class ActionResult:
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

class UseGunAction(Action):
    @override
    def execute(self):
        shell = self.shotgun.eject()
        game_over = False
        skip_turn = False

        if shell is None:
            raise ValueError("Empty chamber, it should be checked on every loop")

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
            raise ValueError(f"No {item} in inventory.")
        self.actor.inventory.items[item] -= 1

    #TODO: Add cases where actions failed to execute raise Exception where necessary

class UseMagnifierAction(ItemAction):
    @override
    def execute(self):
        self._consume_item("magnifier")
        shell = self.shotgun.peek()
        response = f"Current shell is {"Live" if shell else "Blank"}"
        return ActionResult(end_turn=False, response=response)

class UseBeerAction(ItemAction):
    @override
    def execute(self):
        self._consume_item("beer")
        shell = self.shotgun.eject()
        response = f"Current ejected shell is {"Live" if shell else "Blank"}"
        return ActionResult(end_turn=False, response=response)

class UseHandsawAction(ItemAction):
    @override
    def execute(self):
        self._consume_item("handsaw")
        self.shotgun.cutoff()
        return ActionResult(
            end_turn=False, 
            response=f"Doubled shotgun damage, current damage is: {self.shotgun.damage}."
        )

class UseCigaretteAction(ItemAction):
    @override
    def execute(self):
        if self.actor.health < self.stage.health_cap:
            self._consume_item("cigarette")
            self.actor.health += 1
            return ActionResult(end_turn=False, response="Heal user 1 health.")

        return ActionResult(end_turn=False, response="User is at full health.")

class UseHandcuffAction(ItemAction):
    @override
    def execute(self):
        if not self.target.turn:
            return ActionResult(
                end_turn=False, 
                response="Current target's turn has been skipped."
            )

        self._consume_item("handcuff")
        self.target.turn = False
        return ActionResult(
            end_turn=False,
            response="Target's next turn will be skipped."
        )
