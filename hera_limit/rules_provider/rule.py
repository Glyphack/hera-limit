from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Unit(str, Enum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"


@dataclass
class Descriptor:
    key: str
    unit: Unit
    requests_per_unit: int
    value: Optional[str] = None


@dataclass
class Rule:
    path: str
    descriptors: List[Descriptor]

    def match(self, path: str) -> bool:
        return self.path == path
