import copy
import json
import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer

from Code.enums.roles_enum import Role
from Code.enums.game_mode_enum import GameMode
from Code.network.converter_impl import Converter
from Code.network.move_impl import Move
from Code.enums.pin_enum import Pin


class RequestHandler(BaseHTTPRequestHandler):
    code = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE]
    gamemode = GameMode.MASTERMIND

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        request_body = self.rfile.read(content_length)
        print(request_body)
        all_maybe = self.rfile.read()
        print("all maybe: ", all_maybe)
        '''
        # Process the received JSON request
        json_data = json.loads(request_body)
        # Do something with the JSON data
        move = Converter.create_move_from_json(json_data)
        resp_json = None
        if move.game_id == 0:
            print("turn 0")
            move.game_id = 5
            resp_json = Converter.create_json_schema(move)
        else:
            print("normal turn", move.game_id, move.game_id == 0, type(move.game_id))
            pins = move.get_pins()
            feedback = self._make_feedback(RequestHandler.code, pins)
            print(feedback)
            # todo com should generate feedback then replace temp str with resp_json
            feedback_int = Move.get_num_from_pins(feedback)
            print("feedback int: ", feedback_int)
            resp_move = Move(5, 1, 2, 3, feedback_int)
            resp_json = Converter.create_json_schema(resp_move)
        response = resp_json'''
        response = json.dumps("return msg from server")
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode())


def _make_feedback(self, code, last_turn):
    code_temp = copy.deepcopy(code)
    print("make feedback called")
    print("code is: ", type(code_temp))
    print("last turn is: ", type(last_turn))
    print(len(code_temp))
    print(code_temp, last_turn)
    erg = []

    # check if any pins match --> feedback add black
    # remove it, so it doesn't match again
    for i in range(len(code_temp)):
        if last_turn[i] == code_temp[i]:
            erg.append(Pin.BLACK)
            code_temp[i] = None

    # check if any pins match without identical pos
    # --> feedback add white and remove it, so it doesn't match again
    for i in range(len(code_temp)):
        if last_turn[i] in code_temp and last_turn[i] != code_temp[i]:
            erg.append(Pin.WHITE)
            code_temp[code_temp.index(last_turn[i])] = None

    # fill with Holes till the required length is hit
    while len(erg) < self.gamemode.code_length:
        erg.append(Pin.HOLE)
    return erg


def run_server():
    host = 'localhost'
    port = 8000

    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on {host}:{port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
