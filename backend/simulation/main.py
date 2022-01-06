from threading import Thread
from time import sleep

from models.house import House
from models.thermostat import Thermostat


class Simulation:

    def __init__(self):
        self.house = House()
        self.thermostat = Thermostat()
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
        return [room.as_dict() for room in self.house.rooms]

    def get_room(self, room_id: int) -> dict:
        return self.house.get_room_by_id(room_id).as_dict()

    def update_room(self, room_id: int, data: dict):
        room = self.house.get_room_by_id(room_id)
        room.numberOfPeople = data.get('numberOfPeople', room.numberOfPeople)
        room.currentTemperature = data.get('currentTemperature', room.currentTemperature)

    def __run(self):
        while self.is_running:
            for room in self.house.rooms:
                room.change_temperature_due_to_neighbours()
                self.thermostat.regulate_temperature(room)

            sleep(1)
