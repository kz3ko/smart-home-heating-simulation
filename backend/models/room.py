from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
from copy import deepcopy

from models.heater import Heater
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
    wallHeight: float
    density: float  # [g/m^3]
    specificHeat: float  # [J/(g*k)]
    heater: Heater
    toMeterScale: float
    currentTemperature: Optional[float] = 21
    owners: Optional[list[str]] = field(default_factory=list)
    numberOfPeople: Optional[int] = 0
    people: Optional[list[int]] = field(default_factory=list)
    probabilityWeigth: Optional[float] = 1
    neighbours: Optional[dict[str, list[dict[str, int | Room | Backyard]]]] = field(default_factory=lambda: {
        'south': [],
        'north': [],
        'west': [],
        'east': []
    })

    def __post_init__(self):
        self.total_wall_length = 2 * (self.width + self.height)
        self.area = self.__get_area()
        self.volume = self.__get_volume()
        self.mass = self.density * self.volume

    def as_dict(self):
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
            'owner': self.owners,
            'numberOfPeople': self.numberOfPeople,
            'people': self.people,
            'neighbours': neighbours
        }

    def add_person(self, person_id: int):
        self.numberOfPeople += 1
        self.people.append(person_id)

    def remove_person(self, person_id: int):
        self.numberOfPeople -= 1
        self.people.remove(person_id)

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

    def check_if_room_is_a_vertical_neighbour(self, room: Room, wall_thickness: float):
        if abs(self.xPos - room.xPos) <= wall_thickness or abs(
                self.xPos + self.width - room.xPos - room.width) <= wall_thickness:
            if abs(self.yPos - room.height - room.yPos) <= wall_thickness:
                self.set_room_neighbour('north', room)
            elif abs(self.yPos + self.height - room.yPos) <= wall_thickness:
                self.set_room_neighbour('south', room)

    def check_if_room_is_a_horizontal_neighbour(self, room: Room, wall_thickness: float):
        if abs(self.yPos - room.yPos) <= wall_thickness or abs(
                self.yPos + self.height - room.yPos - room.height) <= wall_thickness:
            if abs(self.xPos + self.width - room.xPos) <= wall_thickness:
                self.set_room_neighbour('east', room)
            elif abs(self.xPos - room.width - room.xPos) <= wall_thickness:
                self.set_room_neighbour('west', room)

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

    def __get_area(self):
        return self.toMeterScale ** 2 * self.width * self.height

    def __get_volume(self):
        return self.__get_area() * self.wallHeight
