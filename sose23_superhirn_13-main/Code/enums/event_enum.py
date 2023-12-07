from enum import Enum


class Event(Enum):
    GAMESTATECHANGE = 0
    WINNER = 1
    CHEATER = 2