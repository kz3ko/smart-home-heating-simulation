from models.room import Room
from models.house import House
from models.datetime import Datetime


class Thermostat:

    def __init__(self, house: House, datetime: Datetime):
        self.divider = 4
        self.house = house
        self.datetime = datetime
        self.people_presence_history = {room.id: None for room in self.house}
        self.min_time_without_people = 5

    def regulate_temperature(self, room: Room):
        people = room.numberOfPeople
        last_people_presence = self.people_presence_history[room.id]
        if last_people_presence:
            time_without_people = self.datetime - last_people_presence
        else:
            time_without_people = 0

        if people:
            self.people_presence_history[room.id] = self.datetime
            diff = self.__get_diff_from_optimal_temperature_range(room, time_without_people)
        else:
            diff = self.__get_diff_from_cooldown_temperature(room, time_without_people)

        to_change = diff/self.divider
        room.currentTemperature += to_change

    def __get_diff_from_optimal_temperature_range(self, room: Room, time_without_people: int) -> float:
        optimal_threshold = room.optimalThreshold
        if time_without_people <= self.min_time_without_people:
            diff = max(optimal_threshold) - min(optimal_threshold)
            optimal_threshold = [value + diff/2 for value in optimal_threshold]

        if room.currentTemperature <= min(optimal_threshold):
            return min(optimal_threshold) - room.currentTemperature
        elif room.currentTemperature >= max(room.optimalThreshold):
            return max(optimal_threshold) - room.currentTemperature
        else:
            return 0

    def __get_diff_from_cooldown_temperature(self, room: Room, time_without_people: int) -> float:
        diff = room.cooldownTemperature - room.currentTemperature
        if time_without_people and time_without_people < self.min_time_without_people:
            if 0 > diff > -1:
                return 0
        return diff
