from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from copy import deepcopy

from models.backyard import Backyard


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
    neighbourImpactFactor: float
    currentTemperature: Optional[float] = 21
    previousTemperature: Optional[float] = 21
    owner: Optional[str] = None
    numberOfPeople: Optional[int] = 0
    neighbours: Optional[dict[str, list[dict[str, int | Room | Backyard]]]] = field(default_factory=lambda: {
        'south': [],
        'north': [],
        'west': [],
        'east': []
    })

    def __post_init__(self):
        self.total_wall_length = 2 * (self.width + self.height)
        self.minimal_diff_to_impact = 10 * self.neighbourImpactFactor

    def as_dict(self) -> dict[str, any]:
        neighbours = deepcopy(self.neighbours)
        for neighbours_per_site in neighbours.values():
            if not neighbours_per_site:
                continue
            for neighbour_data in neighbours_per_site:
                neighbour_data.pop('neighbour', None)

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
            'neighbour': neighbours
        }

    def set_room_neighbour(self, site: str, neighbour: Room | Backyard):
        common_wall_length = self.__get_common_wall_length(site, neighbour)
        self.neighbours[site].append({
            'neighbour': neighbour,
            'name': neighbour.name,
            'commonWallLength': common_wall_length
        })
        if isinstance(neighbour, Room):
            self.neighbours[site][-1]['roomId'] = neighbour.id

    def set_backyard_as_lacking_neighbours(self, backyard: Backyard):
        for site in self.neighbours:
            if not self.neighbours[site]:
                self.set_room_neighbour(site, backyard)
                pass

    def check_if_room_is_a_vertical_neighbour(self, room: Room, wall_thickness: int):
        if abs(self.xPos - room.xPos) <= wall_thickness or abs(
                self.xPos + self.width - room.xPos - room.width) <= wall_thickness:
            if abs(self.yPos - room.height - room.yPos) <= wall_thickness:
                self.set_room_neighbour('north', room)
            elif abs(self.yPos + self.height - room.yPos) <= wall_thickness:
                self.set_room_neighbour('south', room)

    def check_if_room_is_a_horizontal_neighbour(self, room: Room, wall_thickness: int):
        if abs(self.yPos - room.yPos) <= wall_thickness or abs(
                self.yPos + self.height - room.yPos - room.height) <= wall_thickness:
            if abs(self.xPos + self.width - room.xPos) <= wall_thickness:
                self.set_room_neighbour('east', room)
            elif abs(self.xPos - room.width - room.xPos) <= wall_thickness:
                self.set_room_neighbour('west', room)

    def change_temperature_due_to_neighbours(self):
        for neighbours_per_site in self.neighbours.values():
            if not neighbours_per_site:
                continue
            for neighbour_data in neighbours_per_site:
                neighbour_room = neighbour_data['neighbour']
                diff = self.currentTemperature - neighbour_room.currentTemperature
                if abs(diff) < self.minimal_diff_to_impact:
                    continue
                common_wall_factor = neighbour_data['commonWallLength']/self.total_wall_length
                to_change = -diff * common_wall_factor * self.neighbourImpactFactor
                self.previousTemperature = self.currentTemperature
                self.currentTemperature += to_change

    def __get_common_wall_length(self, site: str, neighbour: Room | Backyard):
        if site not in self.neighbours.keys():
            raise KeyError(f'Neighbour site should be one of: {self.neighbours.keys()}')

        if isinstance(neighbour, Backyard):
            if site in ['east', 'west']:
                return self.height
            elif site in ['north', 'south']:
                return self.width
        elif isinstance(neighbour, Room):
            if site in ['east', 'west']:
                return min([self.height, neighbour.height])
            elif site in ['north', 'south']:
                return min([self.width, neighbour.width])
        else:
            raise TypeError('Not allowed type of neighbour provided!')
