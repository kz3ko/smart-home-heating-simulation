from dataclasses import dataclass, field
from typing import Optional
from itertools import chain
from random import shuffle, choice
from copy import deepcopy
from math import ceil

from models.datetime import Datetime
from models.house import House
from models.house import Room


@dataclass
class Person:
    id: int
    name: str
    house: House
    datetime: Datetime
    movementProbabilities: dict[str, float]
    currentRoom: Optional[Room] = None
    activities: dict[str, list] = field(default_factory=dict)

    def __post_init__(self):
        self.sleep_time = self.__get_sleep_time()
        self.periods_away_home = self.__get_periods_away_home()
        self.__owned_rooms = [room for room in self.house.rooms if self.id in room.owners]
        self.__foreign_rooms = [room for room in self.house.rooms if room.owners and self.id not in room.owners]
        self.__public_rooms = [room for room in self.house.rooms if not room.owners]
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
        self.__extend(preferred_rooms, self.__public_rooms, self.movementProbabilities['public'])
        self.__extend(preferred_rooms, self.__owned_rooms,  self.movementProbabilities['owned'])
        self.__extend(preferred_rooms, self.__foreign_rooms,  self.movementProbabilities['foreign'])
        shuffle(preferred_rooms)

        return preferred_rooms

    def __extend(self, output_list: list[Room], rooms: list[Room],  probability: float):
        weights = [room.probabilityWeigth for room in rooms]
        weighed_probabilities = {room.id: room.probabilityWeigth / min(weights) for room in rooms}
        output_list.extend(chain(*[[room for _ in range(ceil(
                self.__multiplier * probability * weighed_probabilities[room.id] / sum(weighed_probabilities.values())
        ))] for room in rooms]))
