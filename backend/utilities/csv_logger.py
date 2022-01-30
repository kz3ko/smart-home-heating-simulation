from time import sleep
from os import getcwd, makedirs
from datetime import datetime

from pandas import DataFrame, concat

from config.config import CONFIG
from thread_runner.runner import ThreadRunner
from models.house import House
from models.room import Room
from models.datetime import Datetime

COLUMNS = [
    'timestamp',
    'currentTemperature',
    'targetTemperature',
    'backyardTemperature',
    'heaterPower',
    'maxHeaterPower',
    'numberOfPeople'
]


class CSVLogger(ThreadRunner):

    def __init__(self, logging_interval: float, house: House, datetime_: Datetime):
        super().__init__()
        self.enabled = CONFIG.get('csvLoggerEnabled', False)
        root_path = f'{getcwd()}'
        self.logs_path = f'{root_path}/logs'
        self.logging_interval = logging_interval
        self.house = house
        self.datetime = datetime_
        self.room_dataframes = self.__get_prepared_room_dataframes()
        self.__create_directory(self.logs_path)

    def _run(self):
        log_directory = self.__init_logging_process()
        while self.is_running:
            for room_id, dataframe in self.room_dataframes.items():
                room = self.house.get_room_by_id(room_id)
                latest_data = self.__get_latest_data(room)
                self.room_dataframes[room_id] = concat((self.room_dataframes[room_id], latest_data), ignore_index=True)

            sleep(self.logging_interval)

        self.__save_logs_to_csv(log_directory)

    def start(self):
        if not self.enabled:
            return
        super().start()

    def __init_logging_process(self) -> str:
        timestamp = datetime.now().strftime('%H:%M:%S-%d.%m.%Y')
        log_directory = f'{self.logs_path}/{timestamp}'
        self.__create_directory(log_directory)

        return log_directory

    def __get_latest_data(self, room: Room) -> DataFrame:
        return DataFrame({
            'timestamp': self.datetime,
            'currentTemperature': room.currentTemperature,
            'targetTemperature': 20,
            'backyardTemperature': self.house.backyard.currentTemperature,
            'heaterPower': room.heater.power,
            'maxHeaterPower': room.heater.max_power,
            'numberOfPeople': room.numberOfPeople
        }, index=[0])

    def __save_logs_to_csv(self, log_directory: str):
        for room_id, dataframe in self.room_dataframes.items():
            room = self.house.get_room_by_id(room_id)
            uid = f'{room_id}-{room.name}'
            dataframe.to_csv(f'{log_directory}/{uid}')

    def __get_prepared_room_dataframes(self) -> dict[str, DataFrame]:
        return {room.id: DataFrame(columns=COLUMNS) for room in self.house}

    @staticmethod
    def __create_directory(path: str):
        makedirs(path, exist_ok=True)
