import http.client
import json
from Code.enums.event_enum import Event
from Code.enums.roles_enum import Role
from Code.enums.game_state_enum import GameStates
from Code.enums.pin_enum import Pin
from Code.network.move_impl import Move
from Code.network.converter_impl import Converter


class Network:

    def __init__(self, controller, gamemode, role, gamer_id, ip, port):
        print("new network made")
        self.controller = controller
        self.gamemode = gamemode
        self.role = role
        self.gamer_id = gamer_id
        self.ip = ip
        self.port = port
        self.game_id = self.establish_connection()
        # todo -> delete 5 before actual test w salinger

    def establish_connection(self):
        first_move = Move(game_id=0, gamer_id=self.gamer_id, positions=self.gamemode.code_length,
                          colors=self.gamemode.color_amount, value="")
        scheme = Converter.create_json_schema(move=first_move)
        response = self.post_json(json_object=scheme)

        response_move = Converter.create_move_from_json(response)
        print("new game id:", response_move.game_id)
        return response_move.game_id

    def make_request(self, move):
        # move_temp = Move(game_id=self.game_id, gamer_id=69, positions=4, colors=6, value=1122)
        json_schema = Converter.create_json_schema(move)
        #json_string = json.dumps(json_schema, indent=4)
        return json_schema

    def post_json(self, json_object):
        print("Log: sending obj")
        header = {'Content-type': 'application/json'}
        host = http.client.HTTPConnection(host=self.ip, port=self.port)
        host.request("POST", "/", body=json_object, headers=header)
        print("Log: obj sent")
        response = host.getresponse()
        data = response.read()
        print(data)
        if isinstance(data, bytes):
            data = json.loads(data.decode())
        print("read response")
        return data

    def event_handler(self, event):
        if event == Event.GAMESTATECHANGE:
            if (self.role == Role.CODER) and (self.controller.get_gamestate() == GameStates.CODER_TURN):
                current_move = Move(game_id=self.game_id, gamer_id=self.gamer_id, positions=self.gamemode.code_length,
                                    colors=self.gamemode.color_amount,
                                    value=Move.get_num_from_pins(self.controller.get_last_guess()))
                json_obj = self.make_request(move=current_move)
                response = self.post_json(json_object=json_obj)
                move = Converter.create_move_from_json(json_schema=response)
                self.play_move(move=move)
            else:
                print("role or gamestate is wrong", self.role, self.controller.get_gamestate,
                      self.controller.get_gamestate() == GameStates.CODER_TURN)
        else:
            print("wrong event")

    def play_move(self, move):
        pins = move.get_pins()
        self.controller.check_in_code(self.role, pins)
