from abc import ABC, abstractmethod


class ModelInterface(ABC):

    """
    Model represents current state of the game board.
    Board contains code_list (1 roll with 4 pins), guess_list and feedback_list (both contain 10 rolls with 4 pins each)
    """

    @abstractmethod
    def place_pins(self, colorcode, target_list):
        """
        places the colorcode on the right list in model
        :param colorcode: correct list of pins that should be placed on board.
        :param target_list: list where the colorcode should be placed.
        :return: list of code_list, guess_list, feedback_list, where empty fields are filled with HOLE-Pins
        """
        pass

    @abstractmethod
    def get_board(self):
        """
        :return: list of code_list, guess_list, feedback_list, where empty fields are filled with HOLE-Pins
        """
        pass

    @abstractmethod
    def clear_board(self):
        """
        replaces all pins in board with HOLE-Pins
        """
        pass

    @abstractmethod
    def fill_board(self, game_mode):
        """
        fills board in the beginning of the game with lists of LOCH-Pins.
        :param: game_mode: mode of current game. Length of lists is dependent on game mode.
        """
        pass

    @abstractmethod
    def get_current_turn(self):
        """
        get the current turn x/10
        :return:
        """
        pass
