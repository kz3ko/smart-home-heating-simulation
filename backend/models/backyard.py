from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Backyard:
    currentTemperature: Optional[float] = 0
    previousTemperature: Optional[float] = 0
    city: Optional[str] = 'Cracow'
    name: Optional[str] = 'Backyard'

    def __post_init__(self):
        self.currentTemperature = self.get_current_temperature()

    @staticmethod
    def get_current_temperature() -> float:
        return 21
