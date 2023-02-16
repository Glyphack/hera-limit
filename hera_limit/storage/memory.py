from datetime import datetime, timedelta
from typing import Dict

from hera_limit.storage.storage import AbstractStorage


class Memory(AbstractStorage):
    def __init__(self):
        self.data = {}
        self.ttl: Dict[str, datetime] = {}

    def get(self, key):
        if key in self.ttl:
            if self.ttl[key] < datetime.now():
                del self.ttl[key]
                del self.data[key]
                return None
        return self.data.get(key)

    def set(self, key: str, value: str, ttl_seconds: int):
        self.data[key] = value
        self.ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)

    def incr(self, key: str):
        if key in self.data:
            self.data[key] += 1
        else:
            self.data[key] = 1

    def sorted_set_add(self, key: str, score: float):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(score)

    def sorted_set_remove(self, key: str, start: float, stop: float):
        if key not in self.data:
            return None
        self.data[key] = [x for x in self.data[key] if not (start <= x <= stop)]

    def sorted_set_count(self, key: str, start: int, stop: int):
        if key not in self.data:
            return None
        return len([x for x in self.data[key] if start <= x <= stop])
