class Inventory:
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.items: dict[str, int] = {}

    def is_full(self):
        pass

    def is_empty(self):
        pass

    def has_item(self, item: str):
        return self.items[item] > 0
