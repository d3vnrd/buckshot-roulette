from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from buckshot.entity import Player, Shotgun

class ActionResult:
    def __init__(self):
        self.game_over: bool = False
        self.end_turn: bool = False
        self.chamber_depleted: bool = False

class Action(ABC):
    def __init__(self, actor: Player, target: Player, shotgun: Shotgun):
        self.actor: Player = actor
        self.target: Player = target
        self.shotgun: Shotgun = shotgun
        self.result: ActionResult

    @abstractmethod
    def execute(self) -> Action:
        pass

class UseGunAction(Action):
    @override
    def execute(self):
        return self

class UseMagnifierAction(Action):
    @override
    def execute(self):
        return self

class UseBeerAction(Action):
    @override
    def execute(self):
        return self

class UseHandsawAction(Action):
    @override
    def execute(self):
        return self

class UseCigaretteAction(Action):
    @override
    def execute(self):
        return self

class UseHandcuffAction(Action):
    @override
    def execute(self):
        return self
