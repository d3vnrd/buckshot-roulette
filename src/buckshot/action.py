from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

if TYPE_CHECKING: 
    from buckshot.entity import Player, Shotgun

class Action(ABC):
    def __init__(self, actor: Player):
        self.actor: Player = actor

    @abstractmethod
    def execute(self):
        pass

class ShootAction(Action):
    def __init__(self, actor: Player, target: Player|None, shotgun: Shotgun):
        super().__init__(actor)
        self.target: Player = target or actor
        self.shotgun: Shotgun = shotgun 

    @override
    def execute(self):
        pass

class UseMagnifierAction(Action):
    def __init__(self, actor: Player, shotgun: Shotgun):
        super().__init__(actor)
        self.shotgun: Shotgun = shotgun

    @override
    def execute(self):
        pass

class UseBeerAction(Action):
    def __init__(self, actor: Player, shotgun: Shotgun):
        super().__init__(actor)
        self.shotgun: Shotgun = shotgun

    @override
    def execute(self):
        pass

class UseHandsawAction(Action):
    def __init__(self, actor: Player, shotgun: Shotgun):
        super().__init__(actor)
        self.shotgun: Shotgun = shotgun

    @override
    def execute(self):
        pass

class UseCigaretteAction(Action):
    @override
    def execute(self):
        pass

class UseHandcuffAction(Action):
    def __init__(self, actor: Player, target: Player):
        super().__init__(actor)
        self.target: Player = target

    @override
    def execute(self):
        pass
