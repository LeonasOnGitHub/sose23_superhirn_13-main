import unittest
import unittest
from unittest import mock
from unittest.mock import ANY, MagicMock
from Code.enums.event_enum import Event
from Code.enums.game_state_enum import GameStates
from Code.enums.roles_enum import Role

import numpy as np

import Code.control.controller_impl
from Code.com import com_impl
import random
from Code.enums.pin_enum import Pin
from Code.enums.game_mode_enum import GameMode


def make_com_and_control(gamemode):
    # Create a mock object for the controller
    controller = Code.control.controller_impl.Controller()


class MyTestCase(unittest.TestCase):

    def test_something(self):
        controller = Code.control.controller_impl.Controller()
        com_coder = Code.com.com_impl.Com(controller, Role.CODER, GameMode.MASTERMIND)
        controller.add_listener(com_coder)

        controller.start_game(Role.CODER, GameMode.MASTERMIND, "abed")
        controller.notify_listener(Event.GAMESTATECHANGE, GameStates.GUESSER_TURN)
        print(controller.get_board())


if __name__ == '__main__':
    unittest.main()
