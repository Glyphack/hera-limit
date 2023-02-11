from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, validator


class Unit(str, Enum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"


class Descriptor(BaseModel):
    key: str
    value: Optional[str]
    unit: Unit
    requests_per_unit: int


class Rule(BaseModel):
    path: str
    descriptors: List[Descriptor]

    @validator("descriptors")
    def check_descriptor_not_empty(cls, v):
        if len(v) == 0:
            return ValueError("Descriptor for rule cannot be empty")
