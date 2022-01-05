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
