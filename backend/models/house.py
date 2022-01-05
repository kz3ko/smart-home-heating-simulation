from dataclasses import fields

from config.config import HOUSE_CONFIG
from models.room import Room


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
                room.check_if_room_is_a_vertical_neighbour(neighbour_room, self.wall_thickness)
                room.check_if_room_is_a_horizontal_neighbour(neighbour_room, self.wall_thickness)
