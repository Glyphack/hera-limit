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

    @abstractmethod
    def incr(self, key):
        raise NotImplementedError

    @abstractmethod
    def sorted_set_add(self, key: str, score: float):
        raise NotImplementedError

    @abstractmethod
    def sorted_set_remove(self, key: str, start: float, stop: float):
        raise NotImplementedError

    @abstractmethod
    def sorted_set_count(self, key: str, start: float, stop: float):
        raise NotImplementedError
