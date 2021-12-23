from dataclasses import dataclass
from typing import Optional


@dataclass
class Room:
    name: str
    coldThreshold: [float]
    optimalThreshold: [float]
    warmThreshold: [float]
    hotThreshold: [float]
    cooldownTemperature: float
    owner: Optional[str] = None,
    currentTemperature: Optional[float] = 21
    numberOfPeople: Optional[int] = 0
