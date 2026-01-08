from __future__ import annotations
from dataclasses import dataclass
from collections import deque
import random as rand

class Shotgun:
    @dataclass
    class ShotgunState:
        damage: int
        bullets_left: int
        lives: int
        blanks: int

    def __init__(self):
        self.damage: int = 1
        self.chamber: deque[bool] = deque()

    @property
    def state(self) -> ShotgunState:
        return self.ShotgunState(
            damage=self.damage,
            bullets_left=len(self.chamber),
            lives=self.chamber.count(True),
            blanks=self.chamber.count(False),
        )

    @property
    def is_empty(self) -> bool:
        return len(self.chamber) <=0

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

    def reload(self):
        """Reload new bullets"""
        capacity = rand.randint(3, 8)
        lives = rand.randint(1, capacity // 2)
        blanks = capacity - lives

        self.chamber.clear() # clear chamber before reload
        for bullet in [True] * lives + [False] * blanks:
            self.chamber.append(bullet)
        rand.shuffle(self.chamber)

    def cutoff(self):
        """Double damage dealt"""
        self.damage *= 2

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

    def add(self, n_items: int):
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

class Coordinator:
    """A Circular Queue to manage player's turn"""
    def __init__(self, players: dict[str, Player]) -> None:
        self._queue: deque = deque(set(players.values()))
        rand.shuffle(self._queue)

    def __iter__(self):
        return self

    def __len__(self) -> int:
        return len([p for p in self._queue if p.health > 0])

    def __bool__(self) -> bool:
        """Return True if coordinator has players"""
        return len(self._queue) > 0

    def __next__(self):
        if not self._queue:
            raise StopIteration

        while len(self._queue) > 1:
            player = self._queue.popleft()

            # remove dead player
            if player.health <= 0: 
                continue

            # skip while marking player next turn valid
            if not player.turn: 
                player.turn = True
                self._queue.append(player)
                continue

            self._queue.append(player)
            return player

        # return the last player when queue has 1 player left
        return self._queue.pop()

class Player:
    turn: bool = True # immutable objects are re-created on instance calls

    @dataclass(frozen=True)
    class PlayerState:
        name: str
        health: int
        inventory: dict[str, int]

    def __init__(self, name: str, health: int):
        self.name: str = name
        self.health: int = health
        self.inventory: Inventory = Inventory() # mutable objects however are persisted on every instance calls

    def __hash__(self) -> int:
        """Hash comparison for Set of unique player"""
        return hash(self.name)

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
