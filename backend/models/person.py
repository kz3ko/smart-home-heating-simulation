from dataclasses import dataclass, field
from typing import Optional
from itertools import chain
from random import shuffle, choice
from copy import deepcopy

from models.datetime import Datetime
from models.house import House
from models.house import Room


@dataclass
class Person:
    id: int
    name: str
    house: House
    datetime: Datetime
    currentRoom: Optional[Room] = None
    activities: dict[str, list] = field(default_factory=dict)

    def __post_init__(self):
        self.sleep_time = self.__get_sleep_time()
        self.periods_away_home = self.__get_periods_away_home()
        self.__owned_rooms = [room for room in self.house if self.id in room.owners]
        self.__foreign_rooms = [room for room in self.house if room.owners and self.id not in room.owners]
        self.__public_rooms = [room for room in self.house if not room.owners]
        self.__owned_rooms_move_probability = 0.5
        self.__public_rooms_move_probability = 0.4
        self.__foreign_rooms_move_probability = 0.1
        self.__multiplier = 1000
        self.preferred_rooms = self.__get_preferred_rooms()
        self.move()

    def move(self):
        if self.__is_in_the_house():
            self.__move_when_is_in_the_house()
        else:
            self.__move_when_is_out_the_house()

    def __get_sleep_time(self):
        return self.activities.pop('sleep')[-1].split('-')

    def __get_periods_away_home(self):
        return list(chain(*[[period.split('-') for period in periods] for periods in self.activities.values()]))

    def __is_in_the_house(self):
        if self.name == 'Kate':
            print(self.periods_away_home)
        for start, end in self.periods_away_home:
            if Datetime.from_string(start) <= self.datetime <= Datetime.from_string(end):
                return False
        return True

    def __move_when_is_in_the_house(self):
        room_to_move = self.__get_room_to_move()
        if self.currentRoom == room_to_move:
            return
        if self.currentRoom:
            self.currentRoom.remove_person(self.id)
        self.currentRoom = room_to_move
        self.currentRoom.add_person(self.id)

    def __get_room_to_move(self):
        if self.__check_if_should_sleep():
            if self.currentRoom in self.__owned_rooms:
                return self.currentRoom
            return choice(self.__owned_rooms)
        else:
            return choice(self.preferred_rooms)

    def __check_if_should_sleep(self):
        start, end = self.sleep_time
        start_datetime = Datetime.from_string(start)
        diff = Datetime.from_string(end) - start_datetime
        end_datetime = deepcopy(start_datetime)
        end_datetime.minute += abs(diff)
        end_datetime.synchronize()

        return start_datetime <= self.datetime <= end_datetime

    def __move_when_is_out_the_house(self):
        if self.currentRoom:
            self.currentRoom.remove_person(self.id)
            self.currentRoom = None

    def __get_preferred_rooms(self) -> list[Room]:
        preferred_rooms = []
        self.__extend(preferred_rooms, self.__owned_rooms, self.__multiplier, self.__owned_rooms_move_probability)
        self.__extend(preferred_rooms, self.__foreign_rooms, self.__multiplier, self.__foreign_rooms_move_probability)
        self.__extend(preferred_rooms, self.__public_rooms, self.__multiplier, self.__public_rooms_move_probability)
        shuffle(preferred_rooms)

        return preferred_rooms

    @staticmethod
    def __extend(output_list: list[Room], rooms: list[Room], multiplier: int,  probability: float):
        output_list.extend(
            chain(*[[room for _ in range(int(int(multiplier * probability / len(rooms))))] for room in rooms])
        )


