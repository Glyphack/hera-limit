from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value, ttl_seconds: int):
        pass
