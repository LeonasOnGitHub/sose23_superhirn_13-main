import unittest

from Code.control.controller_impl import Controller
from Code.enums.game_mode_enum import GameMode
from Code.enums.game_state_enum import GameStates
from Code.enums.pin_enum import Pin
from Code.enums.roles_enum import Role

# todo tests with several components!!!!
class TestCaseMMGuesserController(unittest.TestCase):

    def setUp(self):
        self.role = Role.GUESSER
        self.game_mode = GameMode.MASTERMIND
        self.controller = Controller()
        self.empty_board = self.controller.start_game(self.role, self.game_mode)
        self.dummy_code = [Pin.RED, Pin.RED, Pin.RED, Pin.RED]

    '''
        def test_start_game(self):
            dummy_empty_board = [[], [], []]
            empty_line = [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE]
            dummy_empty_board[0] = empty_line
            for i in range(10):
                dummy_empty_board[1].append(empty_line)
                dummy_empty_board[2].append(empty_line)
            self.assertEqual(self.controller.start_game(self.role, self.game_mode), dummy_empty_board)
    '''

    def test_play_again(self):
        self.assertEqual(self.controller.play_again(), self.empty_board)

    def test_get_board_empty(self):
        self.assertEqual(self.controller.get_board(), self.empty_board)

    def test_check_in_code_first(self):
        self.empty_board[1][0] = self.dummy_code
        self.controller.game_state = GameStates.GUESSER_TURN
        self.assertTrue(self.controller.check_in_code(self.role, self.dummy_code))

    def test_check_in_code_all(self):
        for i in range(10):
            self.empty_board[1][i] = self.dummy_code

        for i in range(10):
            self.controller.game_state = GameStates.GUESSER_TURN
            self.controller.check_in_code(self.role, self.dummy_code)

        self.assertEqual(self.controller.get_board(), self.empty_board)

    def test_check_inCode_bad_case_wrong_game_state(self):
        self.controller.game_state = GameStates.START

        self.assertFalse(self.controller.check_in_code(self.role, self.dummy_code))

        self.controller.game_state = GameStates.PLACE_CODE

        self.assertFalse(self.controller.check_in_code(self.role, self.dummy_code))

        self.controller.game_state = GameStates.CODER_TURN

        self.assertFalse(self.controller.check_in_code(self.role, self.dummy_code))

        self.controller.game_state = GameStates.GAME_OVER

        self.assertFalse(self.controller.check_in_code(self.role, self.dummy_code))

    def test_get_last_guess(self):
        self.test_check_in_code_first()
        self.assertEqual(self.controller.get_last_guess(), self.dummy_code)

    def test_win(self):
        # todo check event if player wins
        pass



class TestCaseMMCoderController(unittest.TestCase):

    def setUp(self):
        self.role = Role.CODER
        self.game_mode = GameMode.MASTERMIND
        self.controller = Controller()
        self.empty_board = self.controller.start_game(self.role, self.game_mode)
        self.dummy_feedback = [Pin.WHITE, Pin.WHITE, Pin.HOLE, Pin.HOLE]
        self.dummy_code = [Pin.RED, Pin.RED, Pin.RED, Pin.RED]

    '''
    def test_start_game(self):
        dummy_empty_board = [[], [], []]
        empty_line = [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE]
        dummy_empty_board[0] = empty_line
        for i in range(10):
            dummy_empty_board[1].append(empty_line)
            dummy_empty_board[2].append(empty_line)
        self.assertEqual(self.controller.start_game(self.role, self.game_mode), dummy_empty_board)
    '''
    def test_play_again(self):
        self.assertEqual(self.controller.play_again(), self.empty_board)

    def test_get_board_empty(self):
        self.assertEqual(self.controller.get_board(), self.empty_board)

    def test_check_in_code_final(self):
        self.controller.game_state = GameStates.PLACE_CODE
        self.assertTrue(self.controller.check_in_code(self.role, self.dummy_code))

    '''
    def test_check_in_code_all(self):
        for i in range(10):
            self.empty_board[2][i] = self.dummy_code

        for i in range(10):
            self.controller.game_state = GameStates.CODER_TURN
            self.controller.check_in_code(self.role, self.dummy_code)

        self.assertEqual(self.controller.get_board(), self.empty_board)
    '''

    def test_check_in_feedback(self):
        self.controller.check_in_code(self.role, self.dummy_code)

        self.controller.game_state = GameStates.CODER_TURN
        self.assertTrue(self.controller.check_in_code(self.role, self.dummy_feedback))

    def test_check_inCode_bad_case_wrong_game_state(self):
        self.controller.game_state = GameStates.START

        self.assertFalse(self.controller.check_in_code(self.role, self.dummy_feedback))

        self.controller.game_state = GameStates.PLACE_CODE

        self.assertFalse(self.controller.check_in_code(self.role, self.dummy_feedback))

        self.controller.game_state = GameStates.GAME_OVER

        self.assertFalse(self.controller.check_in_code(self.role, self.dummy_feedback))

    def test_play_again(self):
        self.controller.play_again()

        self.assertEquals(self.controller.listener_list, [])
    def test_win(self):
        # todo check event if player wins
        pass


if __name__ == '__main__':
    unittest.main()
