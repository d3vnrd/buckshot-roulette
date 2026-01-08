from typing import Literal

MsgType = Literal["error", "warn", "done", "info", ""]

class ActionError(Exception):
    def __init__(self, message: str|None = None):
        self.message: str = message or "Action failed"
        super().__init__(self.message)

class EmptyChamberError(ActionError):
    def __init__(self):
        super().__init__("Shotgun chamber should be reloaded if empty on every loop")

class InsufficientItemsError(ActionError):
    def __init__(self, item: str | None = None):
        super().__init__(f"No {item} in inventory")

class InvalidActionError(ActionError):
    def __init__(self, message: str):
        super().__init__(message)
