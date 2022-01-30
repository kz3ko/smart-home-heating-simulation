from time import sleep

from config.config import CONFIG
from thread_runner.runner import ThreadRunner
from models.house import House
from models.thermostat import Thermostat
from models.residents import Residents
from models.datetime import Datetime
from models.backyard import Backyard
from utilities.csv_logger import CSVLogger


class Simulation(ThreadRunner):

    def __init__(self):
        super().__init__()
        self.datetime = Datetime()
        self.backyard = Backyard()
        self.house = House(self.backyard)
        self.residents = Residents(self.house, self.datetime)
        self.thermostat = Thermostat(self.house, self.datetime)
        self.people_move = CONFIG.get('peopleMove', False)
        self.simulation_interval = 1
        self.logger = CSVLogger(self.simulation_interval, self.house, self.datetime)

    def start(self):
        super().start()
        self.logger.start()

    def stop(self):
        super().stop()
        self.logger.stop()

    def set_settings(self, settings: dict[str, any]):
        self.people_move = settings.get('peopleMove', self.people_move)
        self.backyard.currentTemperature = float(settings.get('backyardTemperature', self.backyard.currentTemperature))
        self.logger.enabled = settings.get('csvLoggerEnabled', self.logger.enabled)

    def get_rooms(self) -> list:
        return [room.as_dict() for room in self.house]

    def get_room(self, room_id: int) -> dict:
        return self.house.get_room_by_id(room_id).as_dict()

    def update_room(self, room_id: int, data: dict):
        room = self.house.get_room_by_id(room_id)
        room.numberOfPeople = data.get('numberOfPeople', room.numberOfPeople)
        room.currentTemperature = data.get('currentTemperature', room.currentTemperature)

    def _run(self):
        while self.is_running:
            for room in self.house:
                self.thermostat.regulate_temperature(room)
            if self.people_move:
                for person in self.residents:
                    person.move()
            self.datetime.move()

            sleep(self.simulation_interval)
