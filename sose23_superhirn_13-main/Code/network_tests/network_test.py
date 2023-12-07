import http.client

from Code.network.network_impl import Network
import unittest
import json
from Code.network.network_impl import Move
from unittest.mock import ANY, MagicMock
from Code.enums.roles_enum import Role
from Code.enums.game_mode_enum import GameMode
from Code.enums.pin_enum import Pin
from Code.network.converter_impl import Converter
from Code.enums.event_enum import Event
from Code.enums.game_state_enum import GameStates


class MoveEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Move):
            return obj.__dict__
        return super().default(obj)


class MyTestCase(unittest.TestCase):

    def set_up(self):
        self.ip = 'localhost'
        self.port = 8000
        self.mock_controller = MagicMock()
        # server answer: 1234: red green yellow blue

    ############################  HARDCODED TESTS #######################################

    def post_json_for_testing(self, json_object):
        self.set_up()

        header = {'Content-type': 'application/json'}
        host = http.client.HTTPConnection(host=self.ip, port=self.port)
        host.request("POST", "/", body=json_object, headers=header)  # todo check request body + header standards
        print("Log: obj sent")
        response = host.getresponse()
        data = response.read()
        print(data)
        if isinstance(data, bytes):
            data = json.loads(data.decode())
        print("read response")
        return Converter.create_move_from_json(data)

    def test_init_hardcoded_string_1(self):
        ''' ZUG 0 TEST hartcodiert '''
        move = Move(0, "Abed", 5, 8, "")

        json_obj = Converter.create_json_schema(move)

        response = self.post_json_for_testing(json_object=json_obj)
        print(response)

        return response.game_id

    def test_place_hardcoded_string_1(self):
        game_id = self.test_init_hardcoded_string_1()

        move = Move(game_id, "Abed", 5, 8, "12345")

        json_obj = Converter.create_json_schema(move)

        self.post_json_for_testing(json_object=json_obj)

    def make_sinlge_move(self, game_id):
        move = Move(game_id, "Abed", 4, 6, "1234")

        json_obj = Converter.create_json_schema(move)

        self.post_json_for_testing(json_object=json_obj)

    def test_place_hardcoded_string_10_turn(self):
        game_id = self.test_init_hardcoded_string_1()

        for i in range(10):
            self.make_sinlge_move(game_id)

        return game_id

    def test_place_hardcoded_11th_turn(self):
        game_id = self.test_place_hardcoded_string_10_turn()
        self.make_sinlge_move(game_id)

    ############################ TRUE NETWORK TESTS #######################################

    def test_init_network(self):
        # initializes network
        # todo add test doc
        self.set_up()

        self.mock_controller.check_in_code = MagicMock()
        self.net = Network(self.mock_controller, GameMode.MASTERMIND, Role.CODER, "Abed", self.ip, self.port)
        self.game_id = self.net.game_id

        self.assertFalse(self.net.game_id == 0)

    def test_place_pins_1(self):
        # places first feedback pins
        self.test_init_network()

        self.mock_controller.get_gamestate.side_effect = lambda: GameStates.CODER_TURN
        self.mock_controller.get_last_guess.side_effect = lambda: [Pin.RED, Pin.RED, Pin.GREEN, Pin.GREEN]

        self.net.event_handler(Event.GAMESTATECHANGE)

        self.mock_controller.check_in_code.assert_called()

    # self.mock_controller.check_in_code.assert_called_with([Pin.BLACK, Pin.WHITE, Pin.HOLE, Pin.HOLE])

    def test_place_pins_2(self):
        # places second feedback pins
        self.test_place_pins_1()

        self.mock_controller.get_last_guess.side_effect = lambda: [Pin.GREEN, Pin.RED, Pin.GREEN, Pin.RED]

        self.net.event_handler(Event.GAMESTATECHANGE)

        self.mock_controller.check_in_code.assert_called()

    # self.mock_controller.check_in_code.assert_called_with([Pin.WHITE, Pin.WHITE, Pin.HOLE, Pin.HOLE])

    def test_place_totally_wrong_pins(self):
        # places completely wrong pins
        self.test_place_pins_2()

        self.mock_controller.get_last_guess.side_effect = lambda: [Pin.BROWN, Pin.BROWN, Pin.BROWN, Pin.BROWN]

        self.net.event_handler(Event.GAMESTATECHANGE)

        self.mock_controller.check_in_code.assert_called()
        # self.mock_controller.check_in_code.assert_called_with([Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE])

    def test_place_right_answer(self):
        # places right answer
        self.test_place_pins_2()

        self.mock_controller.get_last_guess.side_effect = lambda: [Pin.BROWN, Pin.GREEN, Pin.ORANGE, Pin.GREEN]

        self.net.event_handler(Event.GAMESTATECHANGE)
        self.mock_controller.check_in_code.assert_called()

    # self.mock_controller.check_in_code.assert_called_with([Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.BLACK])

    def test_place_wrong_event(self):
        # wrong event - network should not react
        self.test_init_network()

        self.net.event_handler("hello")

        self.mock_controller.check_in_code.assert_not_called()

    def test_place_wrong_turn(self):
        # wrong turn - network should not react
        self.test_place_pins_1()

        self.mock_controller.get_gamestate.side_effect = lambda: GameStates.GUESSER_TURN
        self.mock_controller.get_last_guess.side_effect = lambda: [Pin.RED, Pin.RED, Pin.GREEN, Pin.GREEN]

        self.net.event_handler(Event.GAMESTATECHANGE)

        self.mock_controller.check_in_code.assert_not_called()

    def test_move(self):
        move = Move("", "", "", "", 12234)
        print(move.get_pins())


if __name__ == '__main__':
    unittest.main()
