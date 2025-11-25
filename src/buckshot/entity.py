from dataclasses import dataclass
from typing import override
from collections import deque
import random as rand

@dataclass
class Stage:
    health_cap: int = 2
    items_per_reload: int = 1
    gun_capacity: int = 4
    index: int = 1

class Inventory:
    _valid_items: dict[str, int] = {
        "magnifier": 1,
        "beer": 2,
        "handsaw": 3,
        "cigarette": 1,
        "handcuff": 1
    }

    _inv_cap: int = 8

    def __init__(self):
        self.capacity: int = self._inv_cap
        self.items: dict[str, int] = {}

    @property
    def is_full(self) -> bool:
        """Return True if total number of items has reached capacity."""
        return sum(self.items.values()) >= self.capacity

    @property
    def is_empty(self) -> bool:
        """Return True if there are no items at all."""
        return not any(self.items.values())

    @property
    def total(self) -> int:
        return sum(self.items.values())

    def add_items(self, n_items: int):
        """Add multiple random items to inventory."""
        added_items: dict[str, int] = {}
        items_added = 0
        
        while items_added < n_items and not self.is_full:
            available = [
                item for item, cap in self._valid_items.items()
                if self.items.get(item, 0) < cap
            ]
            
            if not available:
                break
            
            item = rand.choice(available)
            self.items[item] = self.items.get(item, 0) + 1
            
            added_items[item] = added_items.get(item, 0) + 1
            items_added += 1
        
        return added_items

    def has_item(self, item: str) -> bool:
        """Check if item is in inventory"""
        return self.items.get(item, 0) > 0

class Shotgun:
    @dataclass
    class ShotgunState:
        damage: int
        bullets_left: int
        lives: int
        blanks: int
        is_empty: bool

    def __init__(self):
        self._damage: int = 1
        self._capacity: int = 0
        self._chamber: deque[bool] = deque()

    @property
    def state(self) -> ShotgunState:
        return self.ShotgunState(
            damage=self._damage,
            bullets_left=len(self._chamber),
            lives=self._chamber.count(True),
            blanks=self._chamber.count(False),
            is_empty=len(self._chamber) <= 0
        )

    def peek(self) -> bool|None:
        """See the next shell in the chamber"""
        if self.state.is_empty:
            return None
        return self._chamber[0]

    def eject(self) -> bool|None:
        """Eject current shell in the chamber"""
        if self.state.is_empty:
            return None
        return self._chamber.pop()

    #TODO: What is the exact rounds for each stage (I, II, & III)
    def reload(self, capacity: int):
        """Reload new bullets"""
        lives = rand.randint(1, 4)
        blanks = capacity - lives

        for bullet in [True] * lives + [False] * blanks:
            self._chamber.append(bullet)
        rand.shuffle(self._chamber)

    def cutoff(self):
        """Double damage dealt"""
        self._damage *= 2

class Player:
    turn: bool = True
    inventory: Inventory = Inventory()

    @dataclass
    class PlayerState:
        name: str
        health: int
        total_items: int
        inv_status: dict[str, int]
        message: str = ""

        def __getitem__(self, key):
            return getattr(self, key)

    def __init__(self, name:str, health:int):
        self.name: str = name
        self.health: int = health

    @property
    def state(self) -> PlayerState:
        return self.PlayerState(
            name=self.name,
            health=self.health,
            total_items=self.inventory.total,
            inv_status=self.inventory.items
        )

    def reset(self, health: int):
        self.health = health
        self.inventory = Inventory()
        self.turn = True

    def get_commands(self) -> list[str]:
        cmds: list[str] = []

        return cmds

class Dealer(Player):
    def __init__(self, health: int):
        super().__init__("Dealer", health)

    @override
    def get_commands(self):
        cmds: list[str] = []

        return cmds
