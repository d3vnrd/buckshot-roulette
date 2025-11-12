from buckshot.entity import Player, Dealer, Shotgun
from buckshot.action import *

VALID_ACTIONS: dict[str, type[Action]] = {
    "magnifier": UseMagnifierAction,
    "beer": UseBeerAction,
    "handsaw": UseHandsawAction,
    "cigarette": UseCigaretteAction,
    "handcuff": UseHandcuffAction,
    "gun": UseGunAction
}

class Stage:
    def __init__(self):
        self.health: int = 2
        self.capacity: int = 4
        self.rounds: int = 4

    def next_stage(self):
        self.health *= 2
        self.capacity *= 2
        self.rounds *= 2

class Board:
    def __init__(self):
        self.shotgun: Shotgun
        self.players : tuple[Player, Player]
        self.stage: Stage
        self.winner: Player|None = None
        self.__curr_idx: int = 0

    @property
    def __ready(self) -> bool:
        if not all(
            hasattr(self, attr) for attr in ["shotgun", "players", "stage"]
        ):
            return False
        
        return all(
            all(hasattr(player, attr) for attr in ["health", "storage", "turn"])
            for player in self.players
        )

    def __parse_cmd(self, args: list[str], actor: Player, target: Player) -> Action:
        cmd = args[0]
        if cmd not in VALID_ACTIONS:
            raise ValueError(f"Invalid command - {cmd}")

        if len(args) > 1 and args[1] == "self":
            target = actor

        return VALID_ACTIONS[cmd](actor, target, self.shotgun)

    def __next_player(self):
        next_player = self.players[1 - self.__curr_idx] 
        
        if not next_player.turn:
            next_player.turn = True
        else:
            self.__curr_idx = 1 - self.__curr_idx

    def __get_winner(self):
        return list(filter(lambda player: player.health > 0, self.players))[0]

    def setup(
        self, 
        player01_name: str,
        player02_name: str,
    ) -> None:
        if self.__ready: 
            raise RuntimeError("Board has already been setup.")

        self.stage = Stage()
        self.shotgun = Shotgun()
        self.players = (
            Player(player01_name),
            Player(player02_name) if player02_name else Dealer()
        )

        self.reset()

    def reset(self):
        if not self.__ready:
            raise RuntimeError("Board have not yet been initialized - call setup() first.")

        self.shotgun.reload(self.stage.rounds)
        for player in self.players:
            player.create(self.stage.health, self.stage.capacity)

    def start(self):
        if not self.__ready:
            raise RuntimeError("Board not ready - call setup() first.")

        while not self.winner:
            actor = self.players[self.__curr_idx]
            target = self.players[1 - self.__curr_idx]

            commands = actor.get_commands()
            try:
                action = self.__parse_cmd(commands, actor, target)
                result = action.execute().result

                if result.game_over:
                    user_input = input("Continue? (yes/no): ")
                    if user_input == "yes":
                        self.stage.next_stage()
                        self.reset()
                        continue
                    else:
                        self.winner = self.__get_winner()

                if result.chamber_depleted:
                    self.shotgun.reload(self.stage.rounds)

                if result.end_turn:
                    self.__next_player()

            except ValueError as e:
                print(f"Error: {e}")
                continue

            except Exception as e:
                print(f"Action failed: {e}")
                continue

        print(f"{self.winner.name} wins!")
