from buckshot.shotgun import Shotgun
from buckshot.player import Entity, Dealer, Player

class Board():
    def __init__(self):
        self.health: int
        self.capacity: int
        self.shotgun: Shotgun
        self.player01: Player
        self.player02: Entity

    def setup(
        self, 
        player01_name: str,
        player02_name: str = "",
        health: int = 2,
        capacity: int = 0,
    ):
        self.shotgun = Shotgun()
        self.player01 = Player(
            player01_name, health, capacity
        )

        if not player02_name:
            self.player02 = Dealer(
                self.player01, health, capacity
            )
        else:
            self.player02 = Player(
                player02_name, health, capacity
            )

    def start(self):
        pass

    def reset(self):
        pass
