from enum import Enum

class Category(Enum):
    Groceries = 1
    Leisure = 2
    Electronics = 3
    Utilities = 4
    Clothing = 5
    Health = 6
    Others = 7

    def names() -> list[str]:
        return [c.name for c in Category]