from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from config.config import CONFIG


@dataclass
class Backyard:
    currentTemperature: Optional[float] = CONFIG.get('backyardTemperature', 21)
    city: Optional[str] = 'Cracow'
    name: Optional[str] = 'Backyard'
