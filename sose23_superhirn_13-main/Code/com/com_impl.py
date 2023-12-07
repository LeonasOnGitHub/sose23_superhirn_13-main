import random
from itertools import combinations, combinations_with_replacement, product

from Code.com.com_interface import ComInterface
import numpy as np
from Code.enums.pin_enum import Pin
import copy
from Code.enums.game_state_enum import GameStates
from Code.enums.event_enum import Event
from Code.enums.roles_enum import Role


class Com(ComInterface):
    feedbacks_const_mm = [
        [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.WHITE, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.WHITE, Pin.WHITE, Pin.HOLE, Pin.HOLE],
        [Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.HOLE],
        [Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.WHITE],
        [Pin.BLACK, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.WHITE, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.HOLE],
        [Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.WHITE],
        [Pin.BLACK, Pin.BLACK, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE],
        [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.BLACK],
    ]

    feedbacks_const_smm = [
        [Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.WHITE, Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.WHITE, Pin.WHITE, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.HOLE, Pin.HOLE],
        [Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.HOLE],
        [Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.WHITE],

        [Pin.BLACK, Pin.HOLE, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.WHITE, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.HOLE],
        [Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.WHITE, Pin.WHITE],

        [Pin.BLACK, Pin.BLACK, Pin.HOLE, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE, Pin.WHITE],

        [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.HOLE, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.HOLE],
        [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.WHITE, Pin.WHITE],

        [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.HOLE],
        # [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.WHITE],

        [Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.BLACK, Pin.BLACK]
    ]

    # controller: Optional[Controller] = None
    def __init__(self, controller, role, gamemode):
        self.controller = controller
        self.role = role
        self.gamemode = gamemode
        if self.gamemode.code_length == 4:
            self.feedbacks_const = Com.feedbacks_const_mm
        if self.gamemode.code_length == 5:
            self.feedbacks_const = Com.feedbacks_const_smm
        self.solution_pool = self._make_all_possible_codes()

    '''
    def _make_possible_feedbacks(self, gamemode):
        # todo returns list of feedbacks w order H->W->B (opposite to what we're used to having. should that be changed?
        code_length = gamemode.code_length

        feedback_values = [pin for pin in Pin if
                           pin in [Pin.HOLE, Pin.BLACK, Pin.WHITE]]  # Filter black, white, and hole pins
        feedback_combinations = []

        # Generate all possible feedback combinations
        for possible_feedback in product(feedback_values, repeat=code_length):

            # if there are no combinations yet, just add the first one, sorted
            if len(feedback_combinations) == 0:
                # todo pin.value deprecated, use pin.number instead
                feedback_combinations.append(list(sorted(possible_feedback, key=lambda x: x.value)))

            # else, convert possible_feedback to list and sort it.
            # then check if combinations contains the possible_feedback.
            # if not, append combinations with possible_feedback
            else:
                # todo pin.value deprecated, use pin.number instead
                sorted_pf = list(sorted(possible_feedback, key=lambda x: x.value))
                if sorted_pf not in feedback_combinations:
                    feedback_combinations.append(sorted_pf)
        return feedback_combinations
    '''

    def _set_controller(self, controller):
        self.controller = controller

    def make_org_code(self):
        if self.role == Role.CODER:
            erg = []
            for i in range(self.gamemode.code_length):
                erg.append(Pin.get_pin_by_number(
                    random.randint(1, self.gamemode.color_amount)))
            self.controller.check_in_code(self.role, erg)

    def _make_feedback(self, code, last_turn):
        code_saved = copy.deepcopy(code)
        last_turn_saved = copy.deepcopy(last_turn)
        erg = []

        # check if any pins match --> feedback add black
        # remove it, so it doesn't match again
        for i in range(len(code_saved)):
            if last_turn_saved[i] == code_saved[i]:
                erg.append(Pin.BLACK)
                code_saved[i] = None
                last_turn_saved[i] = None

        # check if any pins match without identical pos
        # --> feedback add white and remove it, so it doesn't match again
        for i in range(len(code_saved)):
            if last_turn_saved[i] in code_saved and last_turn_saved[i] != code_saved[i]:
                erg.append(Pin.WHITE)
                code_saved[code_saved.index(last_turn_saved[i])] = None  # todo make sure correkt pin is removed,
                # maybe do print of both, should have eq colour
                last_turn_saved[i] = None

        # fill with Holes till the required length is hit
        while len(erg) < self.gamemode.code_length:
            erg.append(Pin.HOLE)

        return erg

    def place_feedback(self):
        if self.role == Role.CODER:
            # get last-played turn and code that the guesser was trying to guess
            last_turn = self.controller.get_last_guess()
            code = self.controller.get_final_code()
            # ("last turn " + str(last_turn))
            # print("code" + str(code))
            # instruct the controller to place the feedback
            self.controller.check_in_code(self.role, self._make_feedback(code, last_turn))

    def _make_all_possible_codes(self):
        pins = [pin for pin in Pin if pin.number in range(1, self.gamemode.color_amount + 1)]
        # todo pin. value is depricated, should be pin.number
        pin_combinations = list(product(pins, repeat=self.gamemode.code_length))
        return np.array(pin_combinations)

    # welches feedback hätten alle möglichen lösungen bei diesem letzten zug generiert
    def _make_feedbacks_of_all_codes(self, last_guess):
        '''
        :param last_guess: ein zug
        :return: Array, mit hypothetischem feedback der möglichen lösungen
        '''
        # todo rm for loop, apply func to all elements of array,
        feedbacks = np.zeros_like(self.solution_pool)
        for index, elem in enumerate(self.solution_pool):
            feedbacks[index] = self._make_feedback(elem.tolist(), last_guess)
        return feedbacks

    def _make_new_solution_pool(self, feedbacks, last_feedback):
        '''
        :param Array, mit hypothetischem feedback der möglichen lösungen
        :param last_feedback: letzte feedbacks
        :return: pool wo nur codes drin sind die dieses feedback generiert hätten
        '''
        return self.solution_pool[np.all(feedbacks == last_feedback, axis=1)]

    def update_possible_moves(self, last_feedback, last_guess):
        feedbacks = self._make_feedbacks_of_all_codes(last_guess)
        # behalte nur lösungs codes die das gegebene feedback bei dieser eingabe generiert hätten
        self.solution_pool = self._make_new_solution_pool(feedbacks, last_feedback)
        print("move amount: ", len(self.solution_pool))
        # note this return is a list and not a nparray, please use self.solution pool for in class use
        return self.solution_pool.tolist()

    def choose_guess(self):
        # self.update_possible_moves(self.controller.get_last_feedback(), self.controller.get_last_guess())
        if self.gamemode.code_length == 4:
            all_turns = self._make_all_possible_codes()
        if self.gamemode.code_length == 5:
            all_turns = copy.deepcopy(self.solution_pool)
        feedbacks14 = self.feedbacks_const
        my_map = {}
        for turn in all_turns:
            IntList = []
            # gen all feedbacks possible solutions would make
            feedbacks = self._make_feedbacks_of_all_codes(turn)
            for feedback in feedbacks14:
                # teile in 14 kategorien
                new_sol_pool = self._make_new_solution_pool(feedbacks, feedback)
                IntList.append(len(new_sol_pool))
            maxInt = max(IntList)  # größe der liste
            # print(tuple(turn))
            # print(type(tuple(turn)))
            my_map[tuple(turn)] = maxInt
        # get the best turn --> its the one with the lowest int mapped to it
        key_with_min_value = min(my_map, key=lambda k: my_map[k])
        # print(key_with_min_value)
        return list(key_with_min_value)

    def event_handler(self, event, detail):
        if Event.GAMESTATECHANGE == event:
            if detail == GameStates.GUESSER_TURN:
                self.guesser_turn()
            if detail == GameStates.CODER_TURN:
                self.place_feedback()
            if detail == GameStates.PLACE_CODE and self.role == Role.CODER:
                self.make_org_code()

    def guesser_turn(self):
        if self.role == Role.GUESSER:
            if self.controller.get_current_turn() != 0:
                print("check", self.controller.get_last_feedback(), self.controller.get_last_guess())
                self.update_possible_moves(self.controller.get_last_feedback(), self.controller.get_last_guess())

            if len(self.solution_pool) == 1:
                print("COM GOT IT")
                self.controller.check_in_code(self.role, self.solution_pool[0])
            elif len(self.solution_pool) == 0:
                print("CHEAT")
                self.controller.notify_listener(Event.CHEATER, None)
                self.controller.check_in_code(self.role, self.solution_pool[0])
            else:
                if self.gamemode.code_length == 4:
                    if self.controller.get_current_turn() == 0:
                        self.controller.check_in_code(self.role, [Pin.YELLOW, Pin.YELLOW, Pin.GREEN, Pin.GREEN])
                    else:
                        self.controller.check_in_code(self.role, self.choose_guess())

                if self.gamemode.code_length == 5:
                    #if self.controller.get_current_turn() == 2:
                    #    self.controller.check_in_code(self.role,
                    #                                  [Pin.YELLOW, Pin.YELLOW, Pin.GREEN, Pin.GREEN, Pin.GREEN])
                    if self.controller.get_current_turn() == 1:
                        self.controller.check_in_code(self.role, [Pin.BLACK, Pin.BLACK, Pin.BLUE, Pin.BLUE, Pin.BLUE])
                    elif self.controller.get_current_turn() == 0:
                        self.controller.check_in_code(self.role, [Pin.RED, Pin.RED, Pin.WHITE, Pin.WHITE, Pin.WHITE])
                    else:
                        self.controller.check_in_code(self.role, self.choose_guess())
