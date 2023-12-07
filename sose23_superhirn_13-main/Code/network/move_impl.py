from Code.enums.pin_enum import Pin


class Move:

    def __init__(self, game_id, gamer_id, positions, colors, value):
        self.game_id = game_id
        self.gamer_id = gamer_id
        self.positions = positions
        self.colors = colors
        self.value = value

    def __str__(self):
        return f"Move(game_id={self.game_id}, gamer_id={self.gamer_id}, positions={self.positions}, colors={self.colors}, value={self.value})"

    def get_pins(self):
        print("get pins called")
        number_list = Move._get_digits(self.value)
        pins = [Pin.get_pin_by_number(num) for num in number_list]
        return pins

    @staticmethod
    def _get_digits(num):
        print("get digits called", num)
        digits = [int(digit) for digit in str(num)]
        return digits

    @staticmethod
    def get_num_from_pins(pins):
        print("pins: ", pins)
        combined_number = int(''.join([str(pin.value) for pin in pins]))
        # todo return right value when pins 0000
        return combined_number
