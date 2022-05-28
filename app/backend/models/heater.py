class Heater:

    def __init__(self, max_power: int):
        self.max_power = max_power
        self.power = 0
        self.is_heating = False

    def __repr__(self):
        return f'Heater with power of: {self.max_power}W'
