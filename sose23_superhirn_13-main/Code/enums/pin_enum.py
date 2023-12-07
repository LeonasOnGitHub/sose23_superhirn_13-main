from enum import Enum


class Pin(Enum):
    HOLE = (0, "lightgrey")
    RED = (1, "red")
    GREEN = (2, "green")
    YELLOW = (3, "yellow")
    BLUE = (4, "blue")
    ORANGE = (5, "orange")
    BROWN = (6, "brown")
    WHITE = (7, "white")
    BLACK = (8, "black")

    def __init__(self, number, color):
        self.number = number
        self.color = color

    @classmethod
    def get_pin_by_number(cls, number):
        for pin in cls:
            if pin.number == number:
                return pin
        return None

    @classmethod
    def get_pin_by_color(cls, color):
        for pin in cls:
            if pin.color == color:
                return pin
        return None
