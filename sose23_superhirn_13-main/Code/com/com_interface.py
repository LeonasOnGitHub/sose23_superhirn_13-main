"""
Defines the behavior of the Com.

The com is a player and uses methods supplied by control to place pins on the board.
can be both a guesser or a coder
"""

from abc import ABC, abstractmethod


class ComInterface(ABC):
    """this is the interface the com should implement."""

    # todo should maybe be renamed to "make_guesser_turn" or "make_gues"
    @abstractmethod
    def update_possible_moves(self, last_feedback, last_guess):
        # WARNING: changed the shit out of this
        """
        Update the possible moves, then makes the next guesser turn by calling check_in_code() method of control.

        if there are no possible moves it calles  notify_listener(self, event, detail) of controll with
        the "show_text" event with the text to display as parameter
        EventBased: called when the game state changes to "guesser_turn"
        control component changes to that state after the coder
        colors are placed
        """
        pass

    @abstractmethod
    def place_feedback(self):
        """
        Generate feedback-Array to the last placed colorcode, then places it on the board.

        todo how is the return value defined? first black then white? what about empty holes?
        EventBased: called when the game state changes to "coder_turn"
        control component changes to that state after the guesser
        colors are placed

        uses the check_in_code() method of control of place the feedback-Array
        uses the get_board_arrays_control() to get the board state
        """
        pass

    # todo should this func not have game state as parameter? so it knows the code length
    @abstractmethod
    def make_org_code(self):
        """
        Generate a new color code then places it on the board with the check_in_code() method of control.

        EventBased: called when the game state changes to "coder_turn"
        control component changes to that state after the guesser
        colors are placed
        """
        pass

# todo get instance and destroy instance method should be here
# todo add observer functions here? on event()? notify()? are they the same?
# should be a switch that then calls the correct internal function
# rm singleton from players
