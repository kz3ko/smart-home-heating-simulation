from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Room:
    name: str
    title: str
    coldThreshold: [float]
    optimalThreshold: [float]
    warmThreshold: [float]
    hotThreshold: [float]
    cooldownTemperature: float
    width: int
    height: int
    xPos: int
    yPos: int
    neighbourRooms: Optional[dict[int, int]] = field(default_factory=dict)
    owner: Optional[str] = None
    currentTemperature: Optional[float] = 21
    numberOfPeople: Optional[int] = 0
