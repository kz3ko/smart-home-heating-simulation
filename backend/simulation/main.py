from threading import Thread
from time import sleep

from models.house import House
from models.thermostat import Thermostat
from models.residents import Residents
from models.datetime import Datetime
from models.backyard import Backyard


class Simulation:

    def __init__(self):
        self.datetime = Datetime()
        self.backyard = Backyard()
        self.house = House(self.backyard)
        self.residents = Residents(self.house, self.datetime)
        self.thermostat = Thermostat(self.house, self.datetime)
        self.is_running = False
        self.simulation_interval = 1
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
        return [room.as_dict() for room in self.house]

    def get_room(self, room_id: int) -> dict:
        return self.house.get_room_by_id(room_id).as_dict()

    def update_room(self, room_id: int, data: dict):
        room = self.house.get_room_by_id(room_id)
        room.numberOfPeople = data.get('numberOfPeople', room.numberOfPeople)
        room.currentTemperature = data.get('currentTemperature', room.currentTemperature)

    def __run(self):
        while self.is_running:
            for room in self.house:
                self.thermostat.regulate_temperature(room)
            for person in self.residents:
                person.move()
            self.datetime.move()

            sleep(self.simulation_interval)
