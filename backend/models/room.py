from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from copy import deepcopy


@dataclass
class Room:
    id: int
    name: str
    title: str
    coldThreshold: list[float]
    optimalThreshold: list[float]
    warmThreshold: list[float]
    hotThreshold: list[float]
    cooldownTemperature: float
    width: int
    height: int
    xPos: int
    yPos: int
    neighbourRoomImpactFactor: float
    currentTemperature: Optional[float] = 21
    owner: Optional[str] = None
    numberOfPeople: Optional[int] = 0
    neighbourRooms: Optional[dict[str, list[dict[str, int | Room]]]] = field(default_factory=lambda: {
        'south': [],
        'north': [],
        'west': [],
        'east': []
    })

    def __post_init__(self):
        self.total_wall_length = 2 * (self.width + self.height)
        self.minimal_diff_to_impact = 10 * self.neighbourRoomImpactFactor

    def as_dict(self):
        neighbour_rooms = deepcopy(self.neighbourRooms)
        for neighbours_per_site in neighbour_rooms.values():
            if not neighbours_per_site:
                continue
            for neighbour_data in neighbours_per_site:
                neighbour_data.pop('room', None)

        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'coldThreshold': self.coldThreshold,
            'optimalThreshold': self.optimalThreshold,
            'warmThreshold': self.warmThreshold,
            'hotThreshold': self.hotThreshold,
            'cooldownTemperature': self.cooldownTemperature,
            'currentTemperature': self.currentTemperature,
            'owner': self.owner,
            'numberOfPeople': self.numberOfPeople,
            'neighbourRooms': neighbour_rooms
        }

    def set_neighbour_room(self, site: str, neighbour_room: Room):
        if site in ['east', 'west']:
            common_wall_length = min([self.height, neighbour_room.height])
        elif site in ['north', 'south']:
            common_wall_length = min([self.width, neighbour_room.width])
        else:
            raise KeyError(f'Neighbour room site should be one of: {self.neighbourRooms.keys()}')

        self.neighbourRooms[site].append({
            'room': neighbour_room,
            'roomId': neighbour_room.id,
            'commonWallLength': common_wall_length
        })

    def check_if_room_is_a_vertical_neighbour(self, room: Room, wall_thickness: int):
        if abs(self.xPos - room.xPos) <= wall_thickness or abs(
                self.xPos + self.width - room.xPos - room.width) <= wall_thickness:
            if abs(self.yPos - room.height - room.yPos) <= wall_thickness:
                self.set_neighbour_room('north', room)
            elif abs(self.yPos + self.height - room.yPos) <= wall_thickness:
                self.set_neighbour_room('south', room)

    def check_if_room_is_a_horizontal_neighbour(self, room: Room, wall_thickness: int):
        if abs(self.yPos - room.yPos) <= wall_thickness or abs(
                self.yPos + self.height - room.yPos - room.height) <= wall_thickness:
            if abs(self.xPos + self.width - room.xPos) <= wall_thickness:
                self.set_neighbour_room('east', room)
            elif abs(self.xPos - room.width - room.xPos) <= wall_thickness:
                self.set_neighbour_room('west', room)

    def change_temperature_due_to_neighbours(self):
        for neighbours_per_site in self.neighbourRooms.values():
            if not neighbours_per_site:
                continue
            for neighbour_data in neighbours_per_site:
                neighbour_room = neighbour_data['room']
                diff = self.currentTemperature - neighbour_room.currentTemperature
                if abs(diff) < self.minimal_diff_to_impact:
                    continue
                common_wall_factor = neighbour_data['commonWallLength']/self.total_wall_length
                to_change = -diff * common_wall_factor * self.neighbourRoomImpactFactor
                self.currentTemperature += to_change

