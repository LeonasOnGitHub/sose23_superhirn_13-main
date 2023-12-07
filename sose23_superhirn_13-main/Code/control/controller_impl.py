from Code.com.com_impl import Com
from Code.enums.event_enum import Event
from Code.enums.game_state_enum import GameStates
from Code.enums.pin_enum import Pin
from Code.enums.roles_enum import Role
from Code.model.model_impl import Model
from Code.control.controller_interface import ControllerInterface
from Code.network.network_impl import Network
from Code.enums.game_mode_enum import GameMode


class Controller(ControllerInterface):
    def __init__(self):
        self.listener_list = []
        self.game_state = GameStates.START
        self.user_role = None
        self.game_mode = None
        self.model = None
        self.gamer_id = None
        self.ip = None
        self.port = None

    def start_game(self, role, game_mode, gamer_id="", ip=None, port=None):
        self.model = Model(game_mode)
        self.game_mode = game_mode
        self.user_role = role
        self.port = port
        self.gamer_id = gamer_id
        self.ip = ip
        self._set_allowed_color_pins()
        self._check_roles_and_create_components(gamer_id, ip, port)
        self.game_state = GameStates.PLACE_CODE
        self.notify_listener(Event.GAMESTATECHANGE, self.game_state)
        return self.get_board()

    def _check_roles_and_create_components(self, gamer_id, ip, port):
        if self.game_mode.online:
            if (ip is not None) and (port is not None):
                # self.network = Network(self, self.game_mode, Role.CODER, gamer_id, ip, port)
                self.add_listener(Network(self, self.game_mode, Role.CODER, gamer_id, ip, port))
                if self.user_role == Role.OBSERVER:
                    # self.com = Com(self, Role.GUESSER, self.game_mode)
                    self.add_listener(Com(self, Role.GUESSER, self.game_mode))
            else:
                raise Exception("ip and port may not be empty!")
        elif self.user_role == Role.CODER:
            # self.com = Com(self, Role.GUESSER, self.game_mode)
            self.add_listener(Com(self, Role.GUESSER, self.game_mode))
        elif self.user_role == Role.GUESSER:
            # self.com = Com(self, Role.CODER, self.game_mode)
            self.add_listener(Com(self, Role.CODER, self.game_mode))
        else:
            raise Exception("something is wrong with your parameters!")

    def _set_allowed_color_pins(self):
        self._allowed_feedback_pins = [Pin.HOLE, Pin.WHITE, Pin.BLACK]
        if self.game_mode.color_amount == 6:
            self._allowed_color_pins = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE, Pin.ORANGE, Pin.BROWN]
        if self.game_mode.color_amount == 8:
            self._allowed_color_pins = [Pin.RED, Pin.GREEN, Pin.YELLOW, Pin.BLUE, Pin.ORANGE, Pin.BROWN, Pin.WHITE,
                                        Pin.BLACK]

    def play_again(self):
        for listener in self.listener_list:
            self.remove_listener(listener)
        self.model.clear_board()
        self.game_state = GameStates.PLACE_CODE
        self.notify_listener(Event.GAMESTATECHANGE, self.game_state)
        return self.get_board()

    def get_board(self):
        return self.model.get_board()

    def check_in_code(self, role, pin_list):
        print("role:", role, "pinlist:", pin_list, "gamestate:", self.game_state)
        if (self.game_state == GameStates.PLACE_CODE) and (role == Role.CODER):
            return self._check_in_final_code(pin_list)
        elif (self.game_state == GameStates.GUESSER_TURN) and (role == Role.GUESSER):
            return self._check_in_guess(pin_list)
        elif (self.game_state == GameStates.CODER_TURN) and (role == Role.CODER):
            return self._check_in_feedback(pin_list)
        return False

    def _check_in_final_code(self, pin_list):
        if len(pin_list) != self.game_mode.code_length:
            return False
        if any(pin not in self._allowed_color_pins for pin in pin_list):
            return False
        self.model.place_pins(pin_list, 0)
        self.game_state = GameStates.GUESSER_TURN
        self.notify_listener(Event.GAMESTATECHANGE, self.game_state)

        return True

    def _check_in_guess(self, pin_list):
        if len(pin_list) != self.game_mode.code_length:
            return False
        if any(pin not in self._allowed_color_pins for pin in pin_list):
            return False
        if self.model.get_current_turn() <= 10:
            self.model.place_pins(pin_list, 1)

        if self._guesser_has_won():
            self.game_state = GameStates.GAME_OVER
            self.notify_listener(Event.GAMESTATECHANGE, self.game_state)
            self.notify_listener(Event.WINNER, Role.GUESSER)
            return True

        self.game_state = GameStates.CODER_TURN
        self.notify_listener(Event.GAMESTATECHANGE, self.game_state)

        return True

    def _check_in_feedback(self, pin_list):
        if len(pin_list) != self.game_mode.code_length:
            return False
        if any(pin not in self._allowed_feedback_pins for pin in pin_list):
            return False
        if self.model.get_current_turn() <= 10:
            #sorts feedback pins in following order B->W->H
            #todo doesnt work!
            sorted_pin_list = sorted(pin_list,
                                     key=lambda x: x.number, reverse=True)
            self.model.place_pins(sorted_pin_list, 2)

        if self.model.get_current_turn() == 10:
            self.game_state = GameStates.GAME_OVER
            self.notify_listener(Event.GAMESTATECHANGE, self.game_state)
            self.notify_listener(Event.WINNER, Role.CODER)
            return True

        self.game_state = GameStates.GUESSER_TURN
        self.notify_listener(Event.GAMESTATECHANGE, self.game_state)

        return True

    def add_listener(self, listener):
        if listener not in self.listener_list:
            self.listener_list.append(listener)

    def remove_listener(self, listener):
        if listener in self.listener_list:
            self.listener_list.remove(listener)

    def notify_listener(self, event, detail):
        for listener in self.listener_list:
            listener.event_handler(event, detail)

    def get_last_guess(self):
        return self.model.get_last_guess()

    def get_last_feedback(self):
        return self.model.get_last_feedback()

    def get_final_code(self):
        return self.model.get_final_code()

    def get_game_state(self):
        return self.game_state

    def _guesser_has_won(self):
        last_guess = self.get_last_guess()
        final_code = self.get_final_code()
        print("guesser has won called")
        for i in range(len(last_guess)):
            if last_guess[i] != final_code[i]:
                return False
        return True

    def get_current_turn(self):
        return self.model.get_current_turn()
