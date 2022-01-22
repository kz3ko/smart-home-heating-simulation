class Heater:

    def __init__(self, max_power: int, lambda_d: float):
        self.max_power = max_power
        self.power = 0
        self.lambda_d = lambda_d
        self.is_heating = False

    def __repr__(self):
        return f'Heater with power of: {self.max_power}W'
