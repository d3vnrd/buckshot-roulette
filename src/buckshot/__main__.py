from buckshot import BuckshotApp, Board

#TODO: add supports for cli commands to quickly setup and play the game
def parse_args():
    pass

if __name__ == "__main__":
    app = BuckshotApp(Board())
    app.run()
