from threading import Thread
from dataclasses import asdict, fields
from time import sleep

from model.room import Room
from config.config import HOUSE_CONFIG


class House:

    def __init__(self):
        self.config = HOUSE_CONFIG
        self.wall_thickness = 20
        self.rooms = self.__get_rooms_from_config()

    def get_room_by_id(self, room_id) -> Room:
        [room] = [room for room in self.rooms if room.id == room_id]
        return room

    def __get_rooms_from_config(self) -> list[Room]:
        rooms = []
        room_field_names = [field.name for field in fields(Room)]
        for room_config in self.config.get('rooms', []):
            valid_room_config = {field: room_config[field] for field in room_config if field in room_field_names}
            try:
                room = Room(**valid_room_config)
            except KeyError:
                raise KeyError(f'There is no id or mandatory parameter for one of the rooms in config!')

            rooms.append(room)

        self.__set_neighbour_rooms(rooms)

        return rooms

    def __set_neighbour_rooms(self, rooms: list[Room]):
        for room in rooms:
            for neighbour_room in rooms:
                if room == neighbour_room:
                    continue
                self.__check_if_it_is_a_vertical_neighbour(room, neighbour_room)
                self.__check_if_it_is_a_horizontal_neighbour(room, neighbour_room)

    def __check_if_it_is_a_vertical_neighbour(self, room: Room, neighbour_room: Room):
        if abs(room.xPos - neighbour_room.xPos) <= self.wall_thickness or abs(
                room.xPos + room.width - neighbour_room.xPos - neighbour_room.width) <= self.wall_thickness:
            if abs(room.yPos - neighbour_room.height - neighbour_room.yPos) <= self.wall_thickness:
                room.set_neighbour_room('north', neighbour_room)
            elif abs(room.yPos + room.height - neighbour_room.yPos) <= self.wall_thickness:
                room.set_neighbour_room('south', neighbour_room)

    def __check_if_it_is_a_horizontal_neighbour(self, room: Room, neighbour_room: Room):
        if abs(room.yPos - neighbour_room.yPos) <= self.wall_thickness or abs(
                room.yPos + room.height - neighbour_room.yPos - neighbour_room.height) <= self.wall_thickness:
            if abs(room.xPos + room.width - neighbour_room.xPos) <= self.wall_thickness:
                room.set_neighbour_room('east', neighbour_room)
            elif abs(room.xPos - neighbour_room.width - neighbour_room.xPos) <= self.wall_thickness:
                room.set_neighbour_room('west', neighbour_room)


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
        return [asdict(room) for room in self.house.rooms]

    def get_room(self, room_id: int) -> dict:
        return asdict(self.house.get_room_by_id(room_id))

    def update_room(self, room_id: int, data: dict):
        room = self.house.get_room_by_id(room_id)
        room.numberOfPeople = data.get('numberOfPeople', room.numberOfPeople)
        room.currentTemperature = data.get('currentTemperature', room.currentTemperature)

    def __run(self):
        while self.is_running:
            for room in self.house.rooms:
                self.sensor.regulate_temperature(room)

            sleep(1)
