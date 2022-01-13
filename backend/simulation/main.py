from threading import Thread
from time import sleep

from models.house import House
from models.thermostat import Thermostat
from models.residents import Residents
from models.datetime import Datetime


class Simulation:

    def __init__(self):
        self.datetime = Datetime()
        self.house = House()
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
        return [room.as_dict() for room in self.house.rooms]

    def get_room(self, room_id: int) -> dict:
        return self.house.get_room_by_id(room_id).as_dict()

    def update_room(self, room_id: int, data: dict):
        room = self.house.get_room_by_id(room_id)
        room.numberOfPeople = data.get('numberOfPeople', room.numberOfPeople)
        room.currentTemperature = data.get('currentTemperature', room.currentTemperature)

    def __run(self):
        while self.is_running:
            for room, heater in zip(self.house.rooms, self.house.heaters):
                room.change_temperature_due_to_neighbours()
                self.thermostat.regulate_temperature(room, heater)
            # for person in self.residents:
            #     person.move()
            self.datetime.move()

            sleep(self.simulation_interval)
