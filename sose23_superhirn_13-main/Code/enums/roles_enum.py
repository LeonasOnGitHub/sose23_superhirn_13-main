from enum import Enum


class Role(Enum):
    CODER = (0, "Codierer")
    GUESSER = (1, "Rater")
    OBSERVER = (2, "Zuschauer")

    def __init__(self, number, description):
        self.number = number
        self.color = description

    @classmethod
    def get_role_by_description(cls, description):
        for pin in cls:
            if pin.color == description:
                return pin
        return None
