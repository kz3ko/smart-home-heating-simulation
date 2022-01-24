from models.room import Room
from models.house import House
from models.datetime import Datetime
from models.air import Air


class Thermostat:

    def __init__(self, house: House, datetime: Datetime):
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

        room.heater.is_heating = (diff > 0)

        heat_balance = self.__get_room_heat_balance(room, diff)

        room.currentTemperature += self.__count_temperature_diff(Air.specific_heat, room.air_mass, heat_balance)

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

    def __get_room_heat_balance(self, room: Room, diff: float) -> float:
        heat_balance = 0
        for neighbours_per_site in room.neighbours.values():
            if not neighbours_per_site:
                continue
            for neighbour_data in neighbours_per_site:
                neighbour = neighbour_data['neighbour']
                temperature_diff = neighbour.currentTemperature - room.currentTemperature
                lambda_d = room.heater.lambda_d
                scale_to_m = 1.5 / 100
                wall_area = scale_to_m * neighbour_data['commonWallLength'] * scale_to_m * room.wallHeight
                heat_balance += self.__count_thermal_conductivity(lambda_d, wall_area, temperature_diff, 1)

        room.heater.power = self.__get_heater_power(room, diff)
        heat_balance += room.heater.power

        return heat_balance * self.datetime.interval * 60

    def __get_heater_power(self, room: Room, diff: float) -> float:
        if not room.heater.is_heating:
            return 0
        to_heat = self.__count_heat_diff(Air.specific_heat, room.air_mass, diff) / (self.datetime.interval * 60)
        if to_heat >= room.heater.max_power:
            return room.heater.max_power
        return to_heat

    @staticmethod
    def __count_thermal_conductivity(lambda_d: float, wall_area: float, temperature_diff: float, time: int) -> float:
        return lambda_d * wall_area * temperature_diff * time

    @staticmethod
    def __count_temperature_diff(specific_heat: float, mass: float, heat_diff: float) -> float:
        return heat_diff / (specific_heat * mass)

    @staticmethod
    def __count_heat_diff(specific_heat: float, mass: float, temperature_diff: float):
        return specific_heat * mass * temperature_diff
