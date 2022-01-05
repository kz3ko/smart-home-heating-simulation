from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Room:
    name: str
    id: int
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
    neighbourRooms: Optional[dict[str, list[dict[str, int]]]] = field(default_factory=lambda: {
        'south': [],
        'north': [],
        'west': [],
        'east': []
    })
    owner: Optional[str] = None
    currentTemperature: Optional[float] = 21
    numberOfPeople: Optional[int] = 0

    def set_neighbour_room(self, site: str, neighbour_room: Room):
        if site in ['east', 'west']:
            common_wall_length = min([self.height, neighbour_room.height])
        elif site in ['north', 'south']:
            common_wall_length = min([self.width, neighbour_room.width])
        else:
            raise KeyError(f'Neighbour room site should be one of: {self.neighbourRooms.keys()}')

        self.neighbourRooms[site].append({
            'neighbourRoomId': neighbour_room.id,
            'neighbourRoomName': neighbour_room.name,
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
