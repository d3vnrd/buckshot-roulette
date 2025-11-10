from buckshot.player import Entity

class Shotgun():
    def __init__(self):
        self.damage: int = 0
        self.chamber: list[bool] = []

    def peek(self) -> str:
        """See the next shell in the chamber"""
        return ""

    def eject(self) -> str:
        """Eject current shell in the chamber"""
        return ""

    def shoot(self, target: Entity) -> None:
        target.health -= self.damage
        if self.damage >= 2:
            self.damage = 1

    def load(self):
        pass

    def status(self):
        """Get current chamber status"""
        return self.chamber.count(True), self.chamber.count(False)

    def double(self) -> None:
        """Double damage dealt"""
        self.damage *= 2

