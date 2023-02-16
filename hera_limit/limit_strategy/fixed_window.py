from datetime import datetime

from hera_limit.limit_strategy.strategy import AbstractStrategy, Request
from hera_limit.rules_provider.rule import Descriptor
from hera_limit.storage.storage import AbstractStorage


class FixedWindow(AbstractStrategy):
    def __init__(
        self,
        storage_backend: AbstractStorage,
        rule_descriptor: Descriptor,
    ):
        super(FixedWindow, self).__init__(storage_backend, rule_descriptor)
        self.interval_len_sec = self.rule_descriptor.unit.to_seconds()
        self.interval_max = self.rule_descriptor.requests_per_unit

    def do_limit(self, request: Request):
        self.request = request
        counter_key = self._get_counter_key()
        if counter_key is None:
            return False
        if self._window_max_reached(counter_key):
            return True

        return False

    def _get_timestamp(self):
        print(datetime.now().timestamp())
        return datetime.now().timestamp()

    def _get_counter_key(self):
        current_interval = str(int(self._get_timestamp() / self.interval_len_sec))
        descriptor = self.rule_descriptor
        path = self.request.path
        key = descriptor.key
        value = self.request.data[key]
        if descriptor.value is not None and value != descriptor.value:
            return None
        else:
            return path + current_interval + "_" + key + "_" + value

    def _window_max_reached(self, counter_key):
        counter = self.storage_backend.get(counter_key)
        if counter is None:
            self.storage_backend.set(counter_key, 1, self.interval_len_sec)
            return False
        elif counter >= self.interval_max:
            return True

        counter += 1
        self.storage_backend.incr(counter_key)

        return False
