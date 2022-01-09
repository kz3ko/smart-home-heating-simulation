from dataclasses import dataclass, field


@dataclass
class Person:
    id: int
    name: str
    activities: list[dict[str, str]] = field(default_factory=list)
