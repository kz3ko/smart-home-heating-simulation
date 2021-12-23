from threading import Thread
from dataclasses import asdict
from time import sleep

from model.room import Room
from config.config import HOUSE_CONFIG


class House:

    def __init__(self):
        self.config = HOUSE_CONFIG
        self.rooms = self.__get_rooms_from_config(self.config)

    @staticmethod
    def __get_rooms_from_config(config: dict) -> dict[str, Room]:
        rooms = {}
        for room_name, room_config in config.get('rooms', {}).items():
            room_config = config['rooms'][room_name]
            try:
                room = Room(
                    name=room_name,
                    coldThreshold=room_config['coldThreshold'],
                    optimalThreshold=room_config['optimalThreshold'],
                    warmThreshold=room_config['warmThreshold'],
                    hotThreshold=room_config['hotThreshold'],
                    cooldownTemperature=room_config['cooldownTemperature'],
                    owner=room_config.get('owner', None),
                    curentTemperature=room_config.get('currentTemperature', 21),
                    numberOfPeople=room_config.get('numberOfPeople', 0)
                )
                rooms[room_config['id']] = room
            except KeyError:
                raise KeyError(f'There is no id, cooldown or threshold temperatures for config of "{room_name}" room!')

        return rooms


class Sensor:

    def __init__(self, rooms: [Room]):
        self.rooms = rooms
        self.minimal_change = 0.05
        self.deviation = 3 * self.minimal_change
        self.divider = 5

    def regulate_temperature(self, room: Room):
        people = room.numberOfPeople
        if people:
            diff = self.__get_diff_from_optimal_temperature_range(room)
        else:
            diff = self.__get_diff_from_cooldown_temperature(room)
        if not diff:
            return
        to_change = self.minimal_change if abs(diff/self.divider) < self.minimal_change else diff/self.divider

        current = room.curentTemperature
        cooldown = room.cooldownTemperature
        if room.name == 'livingRoom':
            print(f'Current: {current}, Cooldown: {cooldown}, Diff: {diff}, To change: {to_change}')

        room.curentTemperature += to_change

    @staticmethod
    def __get_diff_from_optimal_temperature_range(room: Room) -> float:
        current = room.curentTemperature
        min_optimal = min(room.optimalThreshold)
        max_optimal = max(room.optimalThreshold)

        if min_optimal < current < max_optimal:
            return 0
        elif current <= min_optimal:
            diff = min_optimal - current
        else:
            diff = max_optimal - current

    def __get_diff_from_cooldown_temperature(self, room: Room) -> float:
        current = room.curentTemperature
        cooldown = room.cooldownTemperature
        if cooldown - self.deviation < current < cooldown + self.deviation:
            return 0

        diff = abs((cooldown - current)) / self.divider
        to_change = self.minimal_change if diff < self.minimal_change else diff

        return to_change if current < cooldown else -to_change


class Simulation:

    def __init__(self):
        self.house = House()
        self.sensor = Sensor(self.house.rooms)
        self.is_running = False
        self._thread = None

    def start(self):
        self.is_running = True
        if not self._thread:
            self._thread = Thread(target=self.__run, args=(), daemon=True)
            self._thread.start()

    def stop(self):
        self.is_running = False
        if self._thread:
            self._thread = None

    def get_rooms(self) -> list:
        return [asdict(room) for room in self.house.rooms.values()]

    def get_room(self, name: str) -> dict:
        return asdict(self.house.rooms[name])

    def update_room(self, name: str, data: dict):
        room = self.house.rooms[name]
        room.numberOfPeople = data.get('numberOfPeople') or room.numberOfPeople

    def __run(self):
        while self.is_running:
            for room in self.house.rooms.values():
                self.sensor.regulate_temperature(room)
                if room.name == 'livingRoom':
                    print(room)

            sleep(1)
