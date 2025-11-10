from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from buckshot.shotgun import Shotgun
    from buckshot.player import Entity

Target = Shotgun | Entity

class Item(ABC):
    def __init__(self):
        self.amount: int = 0

    @abstractmethod
    def use(self, target: Target) -> str:
        raise NotImplementedError("Error: Subclasses must implement use()")

class Magnifier(Item):
    @override
    def use(self, target: Target) -> str:
        if not isinstance(target, Shotgun):
            raise TypeError("Error: Magnifier can only be used on Shotguns.")

        if target.chamber:
            return f"The next shell is: {target.peek()}"
        return "Current chamber is empty"

class Handsaw(Item):
    @override
    def use(self, target: Target) -> str: 
        if not isinstance(target, Shotgun):
            raise TypeError("Error: Handsaw can only be used on Shotguns.")

        target.double()
        return f"The shotgun barrel has been sawed off! Next shot deals {target.damage}."

class Beer(Item):
    @override
    def use(self, target: Target) -> str:
        if not isinstance(target, Shotgun):
            raise TypeError("Error: Beer can only be used on Shotguns.")

        if target.chamber:
            return f"Ejected a {target.eject()} shell!"
        return "The shotgun is already empty!"

class Cigarette(Item):
    @override
    def use(self, target: Target) -> str:
        if not isinstance(target, Entity):
            raise TypeError("Error: Cigarette can only be used on Player/Dealer.")

        target.health += 1
        return f"{target.name} smokes a cigarette and regains 1 HP."

class Handcuff(Item):
    @override
    def use(self, target: Target) -> str:
        if not isinstance(target, Entity):
            raise TypeError("Error: Handcuff can only be used on Player/Dealer.")

        target.skip()
        return f"{target.name} is handcuffed! They'll miss their next turn."

class Storage:
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.items: dict[str, Item] = {
            "magnifier": Magnifier(),
            "handsaw": Handsaw(),
            "beer": Beer(),
            "cigarette": Cigarette(),
            "handcuff": Handcuff(),
        }

    def is_full(self) -> bool:
        return sum(
            item.amount 
            for item in self.items.values()
        ) >= self.capacity

    def is_empty(self) -> bool:
        return all(
            item.amount == 0 
            for item in self.items.values()
        )

    def get_item(self, item: str) -> Item:
        self.items[item].amount -= 1
        return self.items[item]

    def add(self, item: str) -> bool:
        if item not in self.items:
            raise ValueError("Error: Invalid item input.")

        if self.is_full():
            return False

        self.items[item].amount += 1
        return True

