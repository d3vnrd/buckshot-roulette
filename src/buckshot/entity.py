from collections import deque
import random as rand

class Stage:
    def __init__(self):
        self.health_cap: int = 2
        self.items_per_reload: int = 1
        self.rounds: int = 4
        self.stage_idx: int = 1

    def next_stage(self):
        #TODO: adjust values accodingly
        self.health_cap *= 2
        self.items_per_reload *= 2
        self.rounds *= 2
        self.stage_idx += 1

class Inventory:
    __VALID_ITEMS: dict[str, int] = {
        "magnifier": 1,
        "beer": 2,
        "handsaw": 3,
        "cigarette": 1,
        "handcuff": 1
    }

    __INVENTORY_CAP: int = 8

    def __init__(self):
        self.capacity: int = self.__INVENTORY_CAP
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
                item for item, cap in self.__VALID_ITEMS.items()
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
    def __init__(self):
        self.damage: int = 1
        self.chamber: deque[bool] = deque()

    @property
    def is_empty(self) -> bool:
        return len(self.chamber) <= 0

    def peek(self) -> bool|None:
        """See the next shell in the chamber"""
        if self.is_empty:
            return None
        return self.chamber[0]

    def eject(self) -> bool|None:
        """Eject current shell in the chamber"""
        if self.is_empty:
            return None
        return self.chamber.pop()

    #TODO: What is the exact rounds for each stage (I, II, & III)
    def reload(self, rounds: int):
        """Reload new bullets"""
        lives = rand.randint(1, 4)
        blanks = rounds - lives

        for bullet in [True] * lives + [False] * blanks:
            self.chamber.append(bullet)
        rand.shuffle(self.chamber)

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

    def create(self, health: int):
        self.health = health
        self.inventory = Inventory()
        self.turn = True

    def get_commands(self) -> list[str]:
        cmds: list[str] = []

        return cmds
