from typing import Optional

from models.room import Room
from models.house import House
from models.backyard import Backyard


class Thermostat:

    available_modes = ['heating', 'cooling', None]
    max_gear = 100

    def __init__(self, house: House, backyard: Backyard):
        self.house = house
        self.backyard = backyard
        self.gear = {room.id: 0 for room in self.house.rooms}

    def regulate_temperature(self, room: Room):
        people = room.numberOfPeople
        gear = self.gear[room.id]

        if people:
            diff = self.__get_diff_from_optimal_temperature_range(room)
        else:
            diff = self.__get_diff_from_cooldown_temperature(room)

        gear = self.__get_gear(gear, diff, room)
        mode = self.__get_mode(diff)
        to_change = self.__get_change(gear, diff)

        if mode == 'heating':
            room.currentTemperature += to_change
        elif mode == 'cooling':
            room.currentTemperature -= to_change
        else:
            gear = 0

        self.gear[room.id] = gear

    def __get_gear(self, current_gear: int, temperature_diff: float, room: Room) -> int:
        gear = int(temperature_diff + abs(self.backyard.currentTemperature))
        print(temperature_diff)

        return 67

    @staticmethod
    def __get_mode(temperature_diff: float) -> Optional[str]:
        if temperature_diff > 0:
            return 'heating'
        elif temperature_diff < 0:
            return 'cooling'
        else:
            return None

    @staticmethod
    def __get_change(gear: int, temperature_diff: float):
        change = 0
        if gear >= 10:
            change = (gear - 10) * 0.1
        elif 0 < gear <= 10:
            change = gear * 0.01

        if change > abs(temperature_diff):
            change = abs(temperature_diff)

        return change

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
