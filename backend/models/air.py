from dataclasses import dataclass


@dataclass(frozen=True)
class Air:
    density = 1275  # [g/m^3]
    specific_heat = 1  # [J/(g*k)]
