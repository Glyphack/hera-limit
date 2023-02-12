from abc import ABC, abstractmethod
from enum import Enum


class StorageEngines(str, Enum):
    REDIS = "redis"
    MEMORY = "memory"


class AbstractStorage(ABC):
    @abstractmethod
    def get(self, key):
        raise NotImplementedError

    @abstractmethod
    def set(self, key, value, ttl_seconds: int):
        raise NotImplementedError
