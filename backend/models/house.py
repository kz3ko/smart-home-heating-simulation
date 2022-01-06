from dataclasses import fields

from config.config import HOUSE_CONFIG
from models.room import Room
from models.backyard import Backyard


class House:

    default_wall_thickness = 20  # Equals to 30cm.
    max_wall_thickness = 60  # Equals to 90cm

    def __init__(self, backyard: Backyard):
        self.config = HOUSE_CONFIG
        self.wall_thickness = self.__get_wall_thickness_from_config()
        self.backyard = backyard
        self.neighbour_room_impact_factor = self.wall_thickness/self.max_wall_thickness
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
                room = Room(neighbourImpactFactor=self.neighbour_room_impact_factor, **valid_room_config)
            except KeyError:
                raise KeyError(f'There is no mandatory parameter for one of the rooms in config!')

            rooms.append(room)

        self.__set_room_neighbours(rooms)

        return rooms

    def __get_wall_thickness_from_config(self):
        wall_thickness = self.config.setdefault('wallThickness', self.default_wall_thickness)
        if wall_thickness > self.max_wall_thickness:
            wall_thickness = self.max_wall_thickness
            self.config['wallThickness'] = wall_thickness

        return wall_thickness

    def __set_room_neighbours(self, rooms: list[Room]):
        for room in rooms:
            for neighbour_room in rooms:
                if room == neighbour_room:
                    continue
                room.check_if_room_is_a_vertical_neighbour(neighbour_room, self.wall_thickness)
                room.check_if_room_is_a_horizontal_neighbour(neighbour_room, self.wall_thickness)
            room.set_backyard_as_lacking_neighbours(self.backyard)
