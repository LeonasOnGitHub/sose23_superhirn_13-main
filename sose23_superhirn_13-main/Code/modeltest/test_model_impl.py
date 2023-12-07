import unittest

from Code.enums.pin_enum import Pin
from Code.enums.game_mode_enum import GameMode
from Code.model import model_impl


class GameModeMMTestCase(unittest.TestCase):

    def set_up(self):
        self.model = model_impl.Model(GameMode.MASTERMIND)
        self.dummy_board = [[], [], []]
        empty_line = [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE]
        self.dummy_board[0] = empty_line
        for i in range(10):
            self.dummy_board[1].append(empty_line)
            self.dummy_board[2].append(empty_line)

        self.dummy_final_code = [Pin.RED, Pin.RED, Pin.RED, Pin.RED]
        self.dummy_guesser_code = [Pin.BLUE, Pin.BLUE, Pin.BLUE, Pin.BLUE]
        self.dummy_feedback_code = [Pin.WHITE, Pin.WHITE, Pin.BLACK, Pin.BLACK]

    def test_fill_board(self):
        self.set_up()
        self.assertEqual(self.dummy_board, self.model.get_board())

    def test_place_colorcode_final(self):
        self.set_up()
        self.dummy_board[0][0] = self.dummy_final_code
        self.assertEqual(self.dummy_board, self.model.place_pins(self.dummy_final_code, 0))

    def test_place_colorcode_guess_1(self):
        self.test_place_colorcode_final()
        self.dummy_board[1][0] = self.dummy_guesser_code
        self.assertEqual(self.dummy_board, self.model.place_pins(self.dummy_guesser_code, 1))

    def test_place_pins_all(self):
        self.test_place_colorcode_final()
        for i in range(10):
            self.dummy_board[1][i] = self.dummy_guesser_code
            self.dummy_board[2][i] = self.dummy_feedback_code

        for i in range(10):
            self.model.place_pins(self.dummy_guesser_code, 1)
            self.model.place_pins(self.dummy_feedback_code, 2)
        self.assertEqual(self.dummy_board, self.model.get_board())

    def test_place_colorcode_feedback_1(self):
        self.test_place_colorcode_guess_1()
        self.dummy_board[2][0] = self.dummy_feedback_code
        self.assertEqual(self.dummy_board, self.model.place_pins(self.dummy_feedback_code, 2))


if __name__ == '__main__':
    unittest.main()
