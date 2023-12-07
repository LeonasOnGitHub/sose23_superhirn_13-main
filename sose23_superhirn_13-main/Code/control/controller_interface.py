from abc import ABC, abstractmethod


class ControllerInterface(ABC):
    @abstractmethod
    def start_game(self, role, game_mode, gamer_id="", ip=None, port=None):
        """
        starts new game and creates components depending on game mode
        :param gamer_id: gamer id for online mode. if parameter is left empty, an empty string will be used as gamer id
        :param ip: ip address of network player. must be given for online mode
        :param port: port number of network player. must be given for online mode
        :param game_mode: either local or online game
        :param role: which role Player is taking
        :return: empty board
        :raise: Exception when conflicting parameters
        """
        pass

    @abstractmethod
    def play_again(self):
        """
        starts new game in the same role and same mode
        :return: empty board
        """
        pass

    @abstractmethod
    def get_board(self):
        """
        :return: list of code_list, guess_list, feedback_list
        """
        pass

    @abstractmethod
    def check_in_code(self, role, pin_list):
        # todo update all components, so they work with updated method (NEW PARAMETER: role)
        """
        Checks for correctness and places pins in correct board list depending on game state.
        :param role: role of the component trying to check in code
        :param pin_list: list of pins to be placed on board
        :return: true if pins successfully submitted, else false
        """
        pass

    @abstractmethod
    def _check_in_final_code(self, pin_list):
        """
        Checks for correctness and places code pins on board
        :param pin_list: list from pins to be placed on board
        :return: true if pins successfully placed, false otherwise
        """
        pass

    @abstractmethod
    def _check_in_guess(self, pin_list):
        """
        Checks for correctness and places guess pins on board
        :param pin_list: list from pins to be placed on board
        :return: true if pins successfully placed, false otherwise
        """
        pass

    @abstractmethod
    def _check_in_feedback(self, pin_list):
        """
        Checks for correctness and places feedback pins on board
        :param pin_list: list from pins to be placed on board
        :return: true if pins successfully placed, false otherwise
        """
        pass

    @abstractmethod
    def add_listener(self, listener):
        """
        adds listener to listener list. if listener already in list, do nothing
        :param: listener: listener
        """
        pass

    @abstractmethod
    def remove_listener(self, listener):
        """
        removes listener from listener list. if listener not in the list, do nothing
        :param: listener: listener
        """
        pass

    @abstractmethod
    def notify_listener(self, event, detail):
        """
        notifies all listeners about event by calling their event_handler() method
        :param event: the event that is to be broadcasted, should be a member of th event enum class
        :param detail: details for the broadcasted event
        """
        pass

    @abstractmethod
    def get_last_guess(self):
        """
        :return: last guessed code as a list of pins
        """
        pass

    @abstractmethod
    def get_last_feedback(self):
        """
        :return: last feedback given as list of pins
        """

    @abstractmethod
    def get_game_state(self):
        """
        :return: current game state
        """
        pass

# todo make event-enum
# todo make sound-enum
