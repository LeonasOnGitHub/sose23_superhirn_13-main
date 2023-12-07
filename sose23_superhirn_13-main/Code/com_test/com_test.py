import unittest
from unittest import mock
from unittest.mock import ANY, MagicMock

import numpy as np

from Code.com import com_impl
import random
from Code.enums.pin_enum import Pin
from Code.enums.game_mode_enum import GameMode
from Code.enums.roles_enum import Role


def make_com_and_control_mock(role, gamemode):
    # Create a mock object for the controller
    mock_controller = MagicMock()
    mock_controller.check_in_code = MagicMock()
    #    mock_controller.get_board = MagicMock

    # Create an instance of Com and set the mock controller
    com_obj = com_impl.Com(mock_controller, role, gamemode)
    return com_obj, mock_controller


def get_arrays(arr1, arr2):
    code = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE]
    guesser = [arr1]
    feedback = [arr2]
    return code, guesser, feedback


rand_list = [[6, 1, 1, 6],
             [[3, 2, 2, 2], [6, 1, 6, 6], [5, 1, 5, 4], [1, 1, 1, 2], [2, 5, 5, 1], [5, 2, 6, 6], [6, 5, 4, 2],
              [4, 5, 3, 1], [2, 6, 4, 3], [3, 2, 2, 3]],
             [[7, 7, 8, 7], [8, 8, 9, 8], [7, 9, 8, 9], [7, 8, 7, 9], [8, 9, 9, 8], [9, 7, 9, 7], [7, 9, 7, 8],
              [7, 7, 7, 8], [8, 8, 9, 8], [7, 8, 8, 7]]]


# Create a class for your test cases
class MyTestCase(unittest.TestCase):

    def test_make_org_code(self):
        # Create a mock object for the controller
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER,
                                                             GameMode.MASTERMIND)  # todo nore sure what to do with this parameter
        random.seed(42)
        # Call the method being tested
        com_obj.make_org_code()
        call_args = mock_controller.mock_calls[0][1][1]
        # last one is bcs its saved as a touple and there is only 1 parameter,
        # so it just unpacks it to a list
        for p in call_args:
            print(type(p))
            assert isinstance(p, Pin)
        mock_controller.check_in_code.assert_called()

    def test_place_feedback1(self):  # code, guesser, feedback
        """
        com erstellt feedback zu drei board arrays
        feedback ist leer
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)
        # todo mack mock return arrays when get board state is called
        mock_controller.get_board.side_effect = lambda: rand_list
        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE])

    def test_place_feedback2(self):  # code, guesser, feedback
        """
        com erstellt feedback zu drei board arrays
        Feedback:
        4x Schwarz
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE],
                                             [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.BLACK])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code


        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback3(self):  # code, guesser, feedback
        """
        com erstellt feedback zu drei board arrays
        feedback ist nur weis und leer
        Feedback:
        3x Weiß
        1x Leer
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.GREEN, Pin.RED, Pin.BLUE, Pin.BROWN],
                                             [Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.HOLE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code
        print("print: ", mock_controller.get_board())
        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback4(self):  # code, guesser, feedback
        """
        com erstellt feedback zu drei board arrays
        feedback ist nur weis und schwarz
        Feedback:
        1x Schwarz
        3x Weiß
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.YELLOW, Pin.BLUE, Pin.GREEN],
                                             [Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.WHITE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback5(self):  # code, guesser, feedback
        """
        com erstellt feedback zu drei board arrays
        feedback ist schwarz, weis, leer
        Feedback:
        1x Schwarz
        2x Weiß
        1x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.YELLOW, Pin.GREEN, Pin.BROWN],
                                             [Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.HOLE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback6(self):
        """
        Feedback:
        3x Schwarz
        1x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.YELLOW],
                                             [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.HOLE])

        mock_controller.get_board.return_value = code, guesser, feedback

        com_obj.place_feedback()

        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback7(self):
        """
        Feedback:
        2x Schwarz
        2x Loch
        """

        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.ORANGE, Pin.ORANGE, Pin.YELLOW, Pin.BLUE],
                                             [Pin.BLACK, Pin.BLACK, Pin.HOLE, Pin.HOLE])

        mock_controller.get_board.return_value = code, guesser, feedback

        com_obj.place_feedback()

        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback8(self):
        """
        Feedback:
        4x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.ORANGE, Pin.ORANGE, Pin.ORANGE, Pin.ORANGE],
                                             [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE])

        mock_controller.get_board.return_value = code, guesser, feedback

        com_obj.place_feedback()

        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback9(self):
        '''
        Feedback:
        4x Weiß
        '''
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.BLUE, Pin.YELLOW, Pin.GREEN, Pin.RED],
                                             [Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.WHITE])

        mock_controller.get_board.return_value = code, guesser, feedback

        com_obj.place_feedback()

        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback10(self):  # code, guesser, feedback
        """
        Feedback:
        1x Schwarz
        1x Weiß
        2x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.YELLOW, Pin.BROWN, Pin.BROWN],
                                             [Pin.BLACK, Pin.WHITE, Pin.HOLE, Pin.HOLE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback11(self):  # code, guesser, feedback
        """
        Feedback:
        1x Weiß
        3x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.ORANGE, Pin.ORANGE, Pin.RED, Pin.ORANGE],
                                             [Pin.WHITE, Pin.HOLE, Pin.HOLE, Pin.HOLE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback12(self):  # code, guesser, feedback
        """
        Feedback:
        2x Weiß
        2x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.ORANGE, Pin.YELLOW, Pin.RED, Pin.ORANGE],
                                             [Pin.WHITE, Pin.WHITE, Pin.HOLE, Pin.HOLE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback13(self):
        """
        Feedback:
        1x Schwarz
        3x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.ORANGE, Pin.ORANGE, Pin.ORANGE],
                                             [Pin.BLACK, Pin.HOLE, Pin.HOLE, Pin.HOLE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback14(self):
        """
        Feedback:
        2x Schwarz
        2x Weiß
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.GREEN, Pin.BLUE, Pin.YELLOW],
                                             [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback15(self):
        """
        Feedback:
        2x Schwarz
        1x Weiß
        1x Loch
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.GREEN, Pin.BLUE, Pin.ORANGE],
                                             [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.HOLE])

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function
        mock_controller.check_in_code.assert_called_with(Role.CODER, feedback[0])

    def test_place_feedback0(self):  # code, guesser, feedback # todo maybe this needs to removed
        """
        Länge: 5
        com erstellt feedback zu drei board arrays
        feedback ist schwarz, weis, leer
        """
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.SUPER_MASTERMIND)

        code, guesser, feedback = get_arrays([Pin.RED, Pin.GREEN, Pin.BLUE, Pin.YELLOW, Pin.BROWN],
                                             [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.HOLE])

        code = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE, Pin.ORANGE]
        guesser = [[Pin.RED, Pin.GREEN, Pin.BLUE, Pin.YELLOW, Pin.BROWN]]
        feedback = [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.HOLE]

        mock_controller.get_board.side_effect = lambda: (code, guesser, feedback)
        mock_controller.get_last_guess.side_effect = lambda: guesser[0]
        mock_controller.get_final_code.side_effect = lambda: code

        com_obj.place_feedback()  # todo replace with event based function

    def test_make_all_possible_codes1(self):
        '''
        tested ob alle möglichen kombinationen im mastermind mode als lösung betrachtet werden
        :return:
        '''
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)
        all_codes = com_obj._make_all_possible_codes()
        unique_values = np.unique(all_codes)
        self.assertEquals(len(unique_values), len(all_codes))
        self.assertEquals(1296, len(all_codes))

    def test_make_all_possible_codes1(self):
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.SUPER_MASTERMIND)
        all_codes = com_obj._make_all_possible_codes()
        # unique_values = np.unique(np.array( all_codes))
        # self.assertEquals(len(unique_values), len(all_codes))
        self.assertEquals(32768, len(all_codes))

    def test_update_possible_moves(self):
        '''
        test methode update possible moves
        der letzte zug returned 3 schwarze pins
        es sollten 20 codes weiterhin möglich sein
        '''
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code = [[Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE]]
        guesser_old = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.ORANGE]
        feedback_old = [[Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.HOLE]]

        mock_controller.get_board.side_effect = lambda: (code, guesser_old, feedback_old)
        mock_controller.get_round.side_effect = lambda: 1

        ret = com_obj.update_possible_moves(feedback_old, guesser_old)
        for i in range(len(ret)):
            print("Old Guess: ", guesser_old)
            # print("Feedback old",feedback_old)
            print("kept moves: ", ret[i])
            print("###############################################################################")
        self.assertEquals(20, len(ret))

    def test_update_possible_moves_2(self):
        '''
        test methode update possible moves
        der letzte zug returned 2 schwarze pins 2 weiße pins
        es sollten 5 codes weiterhin möglich sein
        '''
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code = [[Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE]]
        guesser_old = [Pin.RED, Pin.GREEN, Pin.BLUE, Pin.YELLOW]
        feedback_old = [[Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE]]

        mock_controller.get_board.side_effect = lambda: (code, guesser_old, feedback_old)
        mock_controller.get_round.side_effect = lambda: 1

        ret = com_obj.update_possible_moves(feedback_old, guesser_old)
        for i in range(len(ret)):
            print("Old Guess: ", guesser_old)
            # print("Feedback old",feedback_old)
            print("kept moves: ", ret[i])
            print("###############################################################################")
        self.assertEquals(6, len(ret))

    def test_update_possible_moves_3_doppel(self):
        '''
        test methode update possible moves
        es wird zwei mal geupdated
        der letzte zug returned 2 schwarze pins 2 weiße pins
        es sollten 5 codes weiterhin möglich sein
        '''
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        code = [[Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE]]
        guesser_old = [Pin.RED, Pin.GREEN, Pin.BLUE, Pin.YELLOW]
        feedback_old = [[Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE]]

        mock_controller.get_board.side_effect = lambda: (code, guesser_old, feedback_old)
        mock_controller.get_round.side_effect = lambda: 1

        ret = com_obj.update_possible_moves(feedback_old, guesser_old)
        '''        
        for i in range(len(ret)):
            print("Old Guess: ", guesser_old)
            # print("Feedback old",feedback_old)
            print("kept moves: ", ret[i])
            print("###############################################################################") '''
        self.assertEquals(6, len(ret))

        guesser_old = [Pin.BLUE, Pin.GREEN, Pin.RED, Pin.YELLOW]
        feedback_old = [[Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.WHITE]]
        ret2 = com_obj.update_possible_moves(feedback_old, guesser_old)
        '''
        print("\n \n")
        for i in range(len(ret2)):
            print("Old Guess: ", guesser_old)
            # print("Feedback old",feedback_old)
            print("kept moves: ", ret2[i])
            print("###############################################################################") '''
        self.assertEqual(4, len(ret2))

    def test_choose_guess2(self):
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)
        com_obj.choose_guess()

    def test_choose_guess22(self):
        code = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE]
        guess = [Pin.BROWN, Pin.BROWN, Pin.ORANGE, Pin.ORANGE]
        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.MASTERMIND)

        # t1
        feedback = com_obj._make_feedback(code, guess)
        com_obj.update_possible_moves(feedback, guess)

        # t2
        guess = com_obj.choose_guess()
        feedback = com_obj._make_feedback(code, guess)
        com_obj.update_possible_moves(feedback, guess)

        # t3
        guess = com_obj.choose_guess()
        feedback = com_obj._make_feedback(code, guess)
        com_obj.update_possible_moves(feedback, guess)

        # t4
        guess = com_obj.choose_guess()
        feedback = com_obj._make_feedback(code, guess)
        com_obj.update_possible_moves(feedback, guess)

        # t5
        guess = com_obj.choose_guess()
        feedback = com_obj._make_feedback(code, guess)
        com_obj.update_possible_moves(feedback, guess)

    def test_choose_guess_SMM(self):

        com_obj, mock_controller = make_com_and_control_mock(Role.CODER, GameMode.SUPER_MASTERMIND)
        '''   
        code = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE, Pin.ORANGE]
        guess = [Pin.RED, Pin.RED, Pin.RED, Pin.GREEN, Pin.GREEN]

        # t1
        feedback = com_obj._make_feedback(code, guess)
        com_obj.update_possible_moves(feedback, guess)

        # t2
        guess = [Pin.YELLOW, Pin.BLACK, Pin.YELLOW, Pin.BROWN, Pin.WHITE]  # com_obj.choose_guess()
        feedback = com_obj._make_feedback(code, guess)
        ret = com_obj.update_possible_moves(feedback, guess)
        print(ret)
        print(len(ret), "########################################", )
        # t3
        guess = com_obj.choose_guess()
        feedback = com_obj._make_feedback(code, guess)
        ret = com_obj.update_possible_moves(feedback, guess)
        print(ret)
        print(len(ret), "########################################", )
        '''


if __name__ == '__main__':
    unittest.main()
