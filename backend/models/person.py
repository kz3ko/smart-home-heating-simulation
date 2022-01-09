from dataclasses import dataclass, field

from models.datetime import Datetime


@dataclass
class Person:
    id: int
    name: str
    activities: list[dict[str, str]] = field(default_factory=list)

    def move(self, _datetime: Datetime):
        pass
