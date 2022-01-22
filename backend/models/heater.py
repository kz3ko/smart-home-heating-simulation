class Heater:

    def __init__(self, power: int, lambda_d: float):
        self.power = power
        self.lambda_d = lambda_d
        self.is_heating = False

    def __repr__(self):
        return f'Heater with power of: {self.power}W'
