from datetime import datetime, timedelta
from typing import Dict

from hera_limit.storage.storage import AbstractStorage


class Memory(AbstractStorage):
    def __init__(self):
        self.data = {}
        self.ttl: Dict[str, datetime] = {}

    def current_time(self):
        return datetime.now()

    def get(self, key):
        if key in self.ttl:
            if self.ttl[key] < self.current_time():
                del self.ttl[key]
                del self.data[key]
                return None
        return self.data.get(key)

    def set(self, key: str, value: str, ttl_seconds: int):
        self.data[key] = value
        self.ttl[key] = self.current_time() + timedelta(seconds=ttl_seconds)
