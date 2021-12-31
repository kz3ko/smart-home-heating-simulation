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
    def __get_rooms_from_config(config: dict) -> dict[int, Room]:
        rooms = {}
        for room_config in config.get('rooms', []):
            try:
                room = Room(
                    name=room_config['name'],
                    title=room_config['title'],
                    coldThreshold=room_config['coldThreshold'],
                    optimalThreshold=room_config['optimalThreshold'],
                    warmThreshold=room_config['warmThreshold'],
                    hotThreshold=room_config['hotThreshold'],
                    cooldownTemperature=room_config['cooldownTemperature'],
                    owner=room_config.get('owner', None),
                    currentTemperature=room_config.get('currentTemperature', 21),
                    numberOfPeople=room_config.get('numberOfPeople', 0)
                )
                id_ = int(room_config['id'])
            except KeyError:
                raise KeyError(f'There is no mandatory parameter for one of the rooms in config!')

            rooms[id_] = room

        return rooms


class Sensor:

    def __init__(self, rooms: [Room]):
        self.rooms = rooms
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

    def get_room(self, room_id: int) -> dict:
        return asdict(self.house.rooms[room_id])

    def update_room(self, room_id: int, data: dict):
        room = self.house.rooms[room_id]
        room.numberOfPeople = data.get('numberOfPeople', room.numberOfPeople)

    def __run(self):
        while self.is_running:
            for room in self.house.rooms.values():
                self.sensor.regulate_temperature(room)

            sleep(1)
