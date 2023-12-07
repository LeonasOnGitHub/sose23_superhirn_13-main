from Code.model.model_interface import ModelInterface
from Code.enums.game_mode_enum import GameMode
from Code.enums.pin_enum import Pin


class Model(ModelInterface):
    FINAL_CODE_LIST = 0
    GUESSER_LIST = 1
    FEEDBACK_LIST = 2

    def __init__(self, game_mode):
        self._code = None
        self._last_feedback = None
        self._last_guess = None
        self.board = [[], [], []]
        self.fill_board(game_mode)
        self.game_mode = game_mode
        self.current_turn = 0

    def fill_board(self, game_mode):
        if game_mode.code_length == 4:
            empty_line = [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE]
            self.board[0] = empty_line
            for i in range(10):
                self.board[1].append(empty_line)
                self.board[2].append(empty_line)
        elif game_mode.code_length == 5:
            empty_line = [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE]
            self.board[0] = empty_line
            for i in range(10):
                self.board[1].append(empty_line)
                self.board[2].append(empty_line)

    def place_pins(self, colorcode, target_list):
        if target_list == Model.FINAL_CODE_LIST:
            self.board[target_list] = colorcode
        else:
            self.board[target_list][self.current_turn] = colorcode

        if target_list == Model.FINAL_CODE_LIST:
            self._code = colorcode

        if target_list == Model.GUESSER_LIST:
            self._last_guess = colorcode

        if target_list == Model.FEEDBACK_LIST:
            self._last_feedback = colorcode
            self.current_turn += 1

        return self.get_board()

    def get_board(self):
        return self.board

    def clear_board(self):
        self.current_turn = 0
        self.fill_board(self.game_mode)

    def get_current_turn(self):
        return self.current_turn

    def get_last_guess(self):
        return self._last_guess

    def get_last_feedback(self):
        return self._last_feedback

    def get_final_code(self):
        return self._code
