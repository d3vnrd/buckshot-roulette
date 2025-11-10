from buckshot.items import Storage

class Entity():
    def __init__(self, name:str, health: int, capacity: int):
        self.name: str = name
        self.health: int = health
        self.turn: bool = False
        self.storage: Storage = Storage(capacity)

    def skip(self) -> None:
        self.turn = False

class Player(Entity):
    pass

class Dealer(Entity):
    def __init__(
        self, 
        opponent: Entity,
        health: int,
        capacity:int
    ):
        super().__init__("Dealer", health, capacity)
        self.opponent: Entity = opponent

