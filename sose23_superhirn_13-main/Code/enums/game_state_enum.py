from enum import Enum


class GameStates(Enum):
    START = 0
    PLACE_CODE = 1
    GUESSER_TURN = 2
    CODER_TURN = 3
    GAME_OVER = 4
