from dataclasses import dataclass
from typing import Optional


@dataclass
class Room:
    name: str
    target_temperature: float
    cooldown_temperature: float
    owner: Optional[str] = None
    temperature: Optional[float] = 21
    number_of_people: Optional[int] = 0
