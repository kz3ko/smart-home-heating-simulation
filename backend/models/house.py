from dataclasses import fields
from typing import Generator
from enum import Enum

from config.config import HOUSE_CONFIG
from models.room import Room
from models.heater import Heater
from models.backyard import Backyard


class HouseDefaultValues(Enum):
    innerWallThickness = 15  # [cm]
    outerWallThickness = 40  # [cm]
    innerLambda = 1
    outerLambda = 0.2
    wallHeight = 270  # [cm]
    toMeterScale = 0.015


class House:

    def __init__(self, backyard: Backyard):
        self.backyard = backyard
        self.config = HOUSE_CONFIG
        self.to_meter_scale = self.__get_to_meter_scale()
        self.inner_wall_thickness = self.__get_house_meter_value('innerWallThickness')
        self.outer_wall_thickness = self.__get_house_meter_value('outerWallThickness')
        self.wall_height = self.__get_house_meter_value('wallHeight')
        self.inner_lambda = self.__get_lambda_value('innerLambda')
        self.outer_lambda = self.__get_lambda_value('outerLambda')
        self.inner_lambda_d_factor = self.inner_lambda / self.inner_wall_thickness
        self.outer_lambda_d_factor = self.outer_lambda / self.outer_wall_thickness
        self.rooms = self.__get_rooms_from_config()

    def __iter__(self) -> Generator[Room, any, any]:
        for room in self.rooms:
            yield room

    def __repr__(self):
        return f'House with rooms: {", ".join(room.title for room, in self.rooms)}'

    def get_room_by_id(self, room_id) -> Room:
        [room] = [room for room in self.rooms if room.id == room_id]
        return room

    def __get_rooms_from_config(self, ) -> list[Room]:
        rooms = []
        room_field_names = [field.name for field in fields(Room)]
        for room_config in self.config['rooms']:
            valid_room_config = {field: room_config[field] for field in room_config if field in room_field_names}
            try:
                heater = Heater(room_config['heaterPower'])
                room = Room(
                    wallHeight=self.wall_height,
                    heater=heater,
                    toMeterScale=self.to_meter_scale,
                    **valid_room_config
                )
            except KeyError:
                raise KeyError(f'There is no mandatory parameter for one of the rooms in config!')

            rooms.append(room)

        self.__set_room_neighbours(rooms)

        return rooms

    def __set_room_neighbours(self, rooms: list[Room]):
        for room in rooms:
            for neighbour_room in rooms:
                if room == neighbour_room:
                    continue
                room.check_if_room_is_a_vertical_neighbour(neighbour_room)
                room.check_if_room_is_a_horizontal_neighbour(neighbour_room)
            room.set_backyard_as_lacking_neighbours(self.backyard)

    def __get_to_meter_scale(self) -> float:
        return self.config.get('toMeterScale', HouseDefaultValues.toMeterScale.value)

    def __get_house_meter_value(self, name: str) -> float:
        return self.config.get(name, HouseDefaultValues[name]) * self.to_meter_scale

    def __get_lambda_value(self, name) -> float:
        return self.config.get(name, HouseDefaultValues[name])