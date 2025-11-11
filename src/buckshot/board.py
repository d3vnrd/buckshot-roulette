from buckshot.entity import Player, Dealer, Shotgun
from buckshot.action import *

VALID_COMMANDS: dict[str, type[Action]] = {
    "magnifier": UseMagnifierAction,
    "beer": UseBeerAction,
    "handsaw": UseHandsawAction,
    "cigarette": UseCigaretteAction,
    "handcuff": UseHandcuffAction,
    "shoot": ShootAction
}

class Board:
    def __init__(self):
        self.shotgun: Shotgun
        self.player01: Player
        self.player02: Player 

    @property
    def __ready(self) -> bool:
        if not all(hasattr(self, attr) for attr in [
            "shotgun", 
            "player01", 
            "player02"
        ]):
            return False
        
        return all(
            all(hasattr(player, attr) for attr in [
                "health", 
                "storage", 
                "turn"
            ])
            for player in [self.player01, self.player02]
        )

    @property
    def __over(self) -> bool:
        return self.player01.health <= 0 or self.player02.health <= 0

    def __parse_input(self, inputs: str, actor: Player, target: Player):
        pass

    def __execute_action(self, action: Action):
        action.execute()

    def reset(self, health: int, capacity: int):
        if not (self.player01 and self.player02):
            raise RuntimeError("Error: Players have not yet been initialized - call setup() first.")

        self.player01.create(health, capacity)
        self.player02.create(health, capacity)

    def setup(
        self, 
        player01_name: str,
        player02_name: str,
    ) -> None:
        if self.__ready: 
            raise RuntimeError("Error: Board has already been setup.")

        self.shotgun = Shotgun()
        self.player01 = Player(player01_name)
        self.player02 = Player(player02_name) if player02_name else Dealer("Dealer")

        self.reset(2, 4) # Hardcode for first round

    def start(self):
        if not self.__ready:
            raise RuntimeError("Error: Board not ready - call setup() first.")

        players = [self.player01, self.player02]
        turn_idx = 0

        while not self.__over:
            actor = players[turn_idx]

        return "Start"
