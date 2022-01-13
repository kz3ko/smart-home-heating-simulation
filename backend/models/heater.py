from models.room import Room


class Heater:

    def __init__(self, power: int, room: Room, lambda_d: float):
        self.power = power
        self.lambda_d = lambda_d
        self.room = room
        self.is_heating = False

    def __repr__(self):
        return f'Heater with power of: {self.power}W'

    def heat(self, diff: float):
        self.is_heating = True

    def stop_heating(self):
        self.is_heating = False
        pass

    @staticmethod
    def __get_thermal_conductivity(lambda_d: float, s: float, delta_t: float, t: int) -> float:
        return lambda_d * s * delta_t * t

    @staticmethod
    def __get_temperature_difference(q: float, lambda_d: float, s: float, t: int) -> float:
        return q / (s * t * lambda_d)

