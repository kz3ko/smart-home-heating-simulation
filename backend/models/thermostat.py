from models.room import Room


class Thermostat:

    def __init__(self):
        self.divider = 5

    def regulate_temperature(self, room: Room):
        people = room.numberOfPeople
        if people:
            diff = self.__get_diff_from_optimal_temperature_range(room)
        else:
            diff = self.__get_diff_from_cooldown_temperature(room)

        to_change = diff/self.divider
        room.currentTemperature += to_change

    @staticmethod
    def __get_diff_from_optimal_temperature_range(room: Room) -> float:
        if room.currentTemperature <= min(room.optimalThreshold):
            return min(room.optimalThreshold) - room.currentTemperature
        elif room.currentTemperature >= max(room.optimalThreshold):
            return max(room.optimalThreshold) - room.currentTemperature
        else:
            return 0

    @staticmethod
    def __get_diff_from_cooldown_temperature(room: Room) -> float:
        return room.cooldownTemperature - room.currentTemperature
