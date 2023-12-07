import http.client
import json
from Code.enums.event_enum import Event
from Code.enums.roles_enum import Role
from Code.enums.game_state_enum import GameStates
from Code.enums.pin_enum import Pin
from Code.network.move_impl import Move


class Converter:

    @staticmethod
    def create_json_schema(move):
        """
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": "https://htwberlin.com/ssr/superhirnserver/move_schema.json",
            "title": "Move",
            "_comment": "Farbkodierung= 1=Rot, 2=Grün, 3=Gelb, 4=Blau, 5=Orange, 6=Braun, 7=Weiss (Bewertung bzw. Spielfarbe), 8=Schwarz (Bewertung bzw. Spielfarbe)",
            "gameid": {
                "description": int(move.game_id),
                "type": "integer"
            },
            "gamerid": {
                "description": str(move.gamer_id),
                "type": "string"
            },
            "positions": {
                "description": int(move.positions),
                "type": "integer"
            },
            "colors": {
                "description": int(move.colors),
                "type": "integer"
            },
            "value": {
                "description": str(move.value),
                "type": "string"
            },
            "required": ["gameid", "gamerid", "positions", "colors", "value"]
        }
        """

        print("move out: ", move)
        print("move value: ", type(move.value))
        schema = {
            "gameid": int(move.game_id),
            "gamerid": str(move.gamer_id),
            "positions": int(move.positions),
            "colors": int(move.colors),
            "value": str(move.value),
        }
        json_obj = json.dumps(schema)  # todo maybe add indent back?
        print(json_obj)
        return json_obj

    @staticmethod
    def create_move_from_json(json_schema):
        game_id = json_schema["gameid"]
        gamer_id = json_schema["gamerid"]
        positions = json_schema["positions"]
        colors = json_schema["colors"]
        value = json_schema["value"]
        move = Move(game_id=int(game_id), gamer_id=gamer_id, positions=int(positions), colors=int(colors), value=value)
        print("move in: ", move)
        return move
