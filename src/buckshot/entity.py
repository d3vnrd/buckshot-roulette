from typing import override
from collections import deque
import random as rand

class Inventory:
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.items: dict[str, int] = {}

    def is_full(self) -> bool:
        """Return True if total number of items has reached capacity."""
        return sum(self.items.values()) >= self.capacity

    def is_empty(self) -> bool:
        """Return True if there are no items at all."""
        return not any(self.items.values())

    def add(self, item: str) -> None:
        """Add new item into inventory"""
        if item not in self.items:
            self.items[item] = 0
        self.items[item] += 1

    def has_item(self, item: str) -> bool:
        """Check if item is in inventory"""
        return self.items.get(item, 0) > 0

class Shotgun:
    def __init__(self):
        self.damage: int = 1
        self.chamber: deque[bool] = deque()

    def peek(self) -> bool:
        """See the next shell in the chamber"""
        return self.chamber[0]

    def eject(self) -> bool:
        """Eject current shell in the chamber"""
        return self.chamber.pop()

    def reload(self, rounds: int):
        """Reload new bullets"""
        lives = rand.randint(1, 4)
        blanks = rounds - lives

        for bullet in [True] * lives + [False] * blanks:
            self.chamber.append(bullet)

    def stats(self):
        """Get current chamber status"""
        return self.chamber.count(True), self.chamber.count(False)

    def cutoff(self):
        """Double damage dealt"""
        self.damage *= 2

class Player:
    def __init__(self, name:str):
        self.name: str = name
        self.turn: bool
        self.health: int
        self.inventory: Inventory 

    def create(self, health: int, capacity: int):
        self.health = health
        self.inventory = Inventory(capacity)
        self.turn = True

    def get_commands(self) -> list[str]:
        cmds: list[str] = []

        return cmds

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    @override
    def get_commands(self):
        cmds: list[str] = []

        return cmds

