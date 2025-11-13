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

        if shell is True:
            self.target.health -= self.shotgun.damage
            #ERROR: Shotgun damage get reset only if True
            if self.shotgun.damage > 1: 
                self.shotgun.damage = 1
            return ActionResult(game_over= self.target.health <= 0)

        if self.target is self.actor:
            return ActionResult(skip_turn=True)

        return ActionResult()

class ItemAction(Action, ABC):
    def _consume_item(self, item: str):
        if self.actor.inventory.is_empty:
            raise ValueError("Player have no items left.")

        if not self.actor.inventory.has_item(item):
            raise ValueError(f"No {item} in inventory.")
        self.actor.inventory.items[item] -= 1

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

# TODO: Fix Handcuff Action it is quite redundant now
class UseHandcuffAction(ItemAction):
    @override
    def execute(self):
        return ActionResult()
