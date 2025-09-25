from dataclasses import dataclass


@dataclass
class Champion:
    id: int
    name: str
    image: bytes
    missions_count: int = 0
