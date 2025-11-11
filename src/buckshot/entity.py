from buckshot.inventory import Inventory

class Player:
    def __init__(self, name:str):
        self.name: str = name
        self.turn: bool
        self.health: int
        self.inventory: Inventory 

    def create(self, health: int, capacity: int) -> None:
        self.health = health
        self.inventory = Inventory(capacity)
        self.turn = False

class Dealer(Player):
    pass

class Shotgun:
    def __init__(self):
        self.damage: int = 0
        self.chamber: list[bool] = []

    def peek(self) -> str:
        """See the next shell in the chamber"""
        return ""

    def eject(self) -> str:
        """Eject current shell in the chamber"""
        return ""

    def reload(self, n_shells: int = 4):
        """Reload new shells"""
        pass

    def check(self):
        """Get current chamber status"""
        return self.chamber.count(True), self.chamber.count(False)

    def cutoff(self) -> None:
        """Double damage dealt"""
        self.damage *= 2
