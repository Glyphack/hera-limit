from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class Unit(str, Enum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"

    def to_seconds(self) -> int:
        if self == Unit.SECOND:
            return 1
        elif self == Unit.MINUTE:
            return 60
        elif self == Unit.HOUR:
            return 3600
        else:
            raise ValueError(f"Unknown unit: {self}")


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
