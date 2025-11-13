from buckshot.entity import Player, Dealer, Shotgun, Stage
from buckshot.action import *

VALID_ACTIONS: dict[str, type[Action]] = {
    "magnifier": UseMagnifierAction,
    "beer": UseBeerAction,
    "handsaw": UseHandsawAction,
    "cigarette": UseCigaretteAction,
    "handcuff": UseHandcuffAction,
    "gun": UseGunAction
}

class Board:
    def __init__(self):
        self.shotgun: Shotgun
        self.players : tuple[Player, Player]
        self.stage: Stage
        self.winner: Player|None = None
        self._curr_idx: int = 0

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

        return VALID_ACTIONS[cmd](actor, target, self.shotgun, self.stage)

    def __next_player(self, next_player: Player):
        if not next_player.turn:
            next_player.turn = True
        else:
            self._curr_idx = 1 - self._curr_idx

    def __add_items(self):
        return (
            player.inventory.add_items(self.stage.items_per_reload)
            for player in self.players
        )

    def __get_winner(self):
        return list(filter(lambda player: player.health > 0, self.players))[0]

    def __reset(self):
        self.shotgun.reload(self.stage.rounds)
        for player in self.players:
            player.create(self.stage.health_cap)

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

        self.__reset()

    def start(self):
        if not self.__ready:
            raise RuntimeError("Board not ready - call setup() first.")

        while not self.winner:
            actor = self.players[self._curr_idx]
            target = self.players[1 - self._curr_idx]

            # This make sure that shotgun chamber will never be empty
            if self.shotgun.is_empty:
                self.shotgun.reload(self.stage.rounds)
                if self.stage.stage_idx > 1:
                    #TODO: Need a handler to notify user items being added
                    _ = self.__add_items()

            commands = actor.get_commands() # Return item use (gun/items) and target if required
            try:
                action = self.__parse_cmd(commands, actor, target)
                result = action.execute()

                if result.game_over:
                    user_input = input("Continue? (yes/no): ")
                    if user_input == "yes":
                        self.stage.next_stage()
                        self.__reset()
                        continue
                    else:
                        self.winner = self.__get_winner()
                        continue

                if result.skip_turn:
                    target.turn = False

                if result.end_turn:
                    self.__next_player(target)

            #TODO: Add handler to pass Exception to display manager
            except ValueError as e:
                print(f"Error: {e}")
                continue

            except Exception as e:
                print(f"Action failed: {e}")
                continue

        #TODO: Add handler to pass Winner to displayer manager
        print(f"{self.winner.name} wins!")
