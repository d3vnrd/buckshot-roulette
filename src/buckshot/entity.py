from dataclasses import dataclass
from collections import deque
import random as rand

@dataclass
class Stage:
    health_cap: int = 3 # I: 3, II: 4, III: 5
    items_per_reload: int = 1 # I: 2, II: 4, III: 4
    index: int = 1
    turn: int = 0

class Shotgun:
    @dataclass
    class ShotgunState:
        damage: int
        bullets_left: int
        lives: int
        blanks: int

    def __init__(self):
        self._damage: int = 1
        self._chamber: deque[bool] = deque()

    @property
    def state(self) -> ShotgunState:
        return self.ShotgunState(
            damage=self._damage,
            bullets_left=len(self._chamber),
            lives=self._chamber.count(True),
            blanks=self._chamber.count(False),
        )

    @property
    def is_empty(self) -> bool:
        return len(self._chamber) <=0

    def peek(self) -> bool|None:
        """See the next shell in the chamber"""
        if self.is_empty:
            return None
        return self._chamber[0]

    def eject(self) -> bool|None:
        """Eject current shell in the chamber"""
        if self.is_empty:
            return None
        return self._chamber.pop()

    def reload(self):
        """Reload new bullets"""
        capacity = rand.randint(3, 8)
        lives = rand.randint(1, capacity // 2)
        blanks = capacity - lives

        self._chamber.clear() # clear chamber before reload
        for bullet in [True] * lives + [False] * blanks:
            self._chamber.append(bullet)
        rand.shuffle(self._chamber)

    def cutoff(self):
        """Double damage dealt"""
        self._damage *= 2

class Inventory:
    MAX_CAPACITY: int = 8
    VALID_ITEMS: dict[str, int] = {
        "magnifier": 1,
        "beer": 2,
        "handsaw": 3,
        "cigarette": 1,
        "handcuff": 1
    }

    def __init__(self) -> None:
        self.items: dict[str, int] = {
            "magnifier": 0,
            "beer": 0,
            "handsaw": 0,
            "cigarette": 0,
            "handcuff": 0
        }

    @property
    def is_full(self) -> bool:
        """Return True if total number of items has reached capacity."""
        return sum(self.items.values()) >= self.MAX_CAPACITY

    @property
    def total(self) -> int:
        return sum(self.items.values())

    def add_items(self, n_items: int):
        """Add N random items to inventory."""
        added_items: dict[str, int] = {}
        items_added = 0
        
        while items_added < n_items and not self.is_full:
            available = [
                item for item, cap in self.VALID_ITEMS.items()
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

class Player:
    turn: bool = True # immutable objects are re-created on instance calls

    @dataclass
    class PlayerState:
        name: str
        health: int
        inventory: dict[str, int]

    def __init__(self, name:str, health:int):
        self.name: str = name
        self.health: int = health
        self.inventory: Inventory = Inventory() # mutable objects however are persisted on every instance calls

    @property
    def state(self) -> PlayerState:
        return self.PlayerState(
            name = self.name,
            health = self.health,
            inventory = self.inventory.items
        )

    def reset(self, health: int):
        self.health = health
        self.inventory = Inventory()
        self.turn = True

class Dealer(Player):
    def __init__(self, health: int):
        super().__init__("Dealer", health)
