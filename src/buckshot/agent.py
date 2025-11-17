from typing import override
from .entity import Player

class Dealer(Player):
    def __init__(self):
        super().__init__("Dealer")

    @override
    def get_commands(self):
        cmds: list[str] = []

        return cmds

class GeminiAgent(Player):
    def __init__(self):
        super().__init__("Gemini")

    @override
    def get_commands(self):
        cmds: list[str] = []

        return cmds
