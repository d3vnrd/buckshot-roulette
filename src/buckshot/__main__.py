from buckshot import Interface, GameBoard

#TODO: add supports for cli commands to quickly setup and play the game
def parse_args():
    pass

#TODO: create observer class to bridge between iterface and logic handler
class Buckshot:
    def __init__(self, args: list[str] | None = None) -> None:
        self.ui: Interface = Interface(args)
        self.board: GameBoard = GameBoard()

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    buckshot = Buckshot()
    buckshot.run()
