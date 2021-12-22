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
                target_temperature = room_config['target_temperature']
                cooldown_temperature = room_config['cooldown_temperature']
            except KeyError:
                raise KeyError(f'There is no target or cooldown temperature field in config for {room_name} room!')
            owner = room_config.get('owner', None)
            room = Room(room_name, target_temperature, cooldown_temperature, owner)
            rooms[room_name] = room

        return rooms


class Sensor:

    def __init__(self, house: House):
        self.house = house
        self.deviation = 0.2

    def regulate_temperature(self, room: Room):
        current = room.temperature
        people = room.number_of_people
        target = room.cooldown_temperature if people == 0 else room.target_temperature

        if target - self.deviation < current < target + self.deviation:
            return

        diff = abs(current - target) / 3
        if diff < self.deviation:
            diff = self.deviation

        if current < target:
            room.temperature += diff
        if current > target:
            room.temperature -= diff


class Simulation:

    def __init__(self):
        self.house = House()
        self.sensor = Sensor(self.house)
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

    def set_room_data(self, name: str, data: dict):
        room = self.house.rooms[name]
        room.number_of_people = data.get('numberOfPeople') or room.number_of_people

    def __run(self):
        while self.is_running:
            for room in self.house.rooms.values():
                self.sensor.regulate_temperature(room)

            sleep(1)
