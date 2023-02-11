from datetime import datetime, timedelta
from typing import Dict


class Memory:
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
