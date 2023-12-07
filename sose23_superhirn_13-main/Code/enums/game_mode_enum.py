from enum import Enum


class GameMode(Enum):
    SUPER_MASTERMIND = (5, 8, False)
    ONLINE_SUPER_MASTERMIND = (5, 8, True)
    MASTERMIND = (4, 6, False)
    ONLINE_MASTERMIND = (4, 6, True)

    def __init__(self, code_length, color_amount, online):
        self.code_length = code_length
        self.color_amount = color_amount
        self.online = online
