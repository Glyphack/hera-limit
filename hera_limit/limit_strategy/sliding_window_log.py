from datetime import datetime

from hera_limit.limit_strategy.strategy import AbstractStrategy, Request
from hera_limit.rules_provider.rule import Descriptor
from hera_limit.storage.storage import AbstractStorage


class SlidingWindowLog(AbstractStrategy):
    def __init__(
        self,
        storage_backend: AbstractStorage,
        rule_descriptor: Descriptor,
    ):
        super(SlidingWindowLog, self).__init__(storage_backend, rule_descriptor)
        self.interval_len_sec = self.rule_descriptor.unit.to_seconds()
        self.interval_max = self.rule_descriptor.requests_per_unit

    def do_limit(self, request: Request):
        self.request = request
        window_key = self._get_window_key()
        if window_key is None:
            return False
        if self._window_max_reached(window_key):
            return True

        return False

    def _get_window_key(self):
        descriptor = self.rule_descriptor
        path = self.request.path
        key = descriptor.key
        value = self.request.data[key]
        if descriptor.value is not None and value != descriptor.value:
            return None
        else:
            return path + "_" + key + "_" + value

    def _window_max_reached(self, window_key):
        self.storage_backend.sorted_set_remove(
            window_key,
            0,
            datetime.now().timestamp() - self.interval_len_sec,
        )
        current_window_req_count = self.storage_backend.sorted_set_count(
            window_key,
            datetime.now().timestamp() - self.interval_len_sec,
            datetime.now().timestamp(),
        )
        if current_window_req_count is None:
            self.storage_backend.sorted_set_add(window_key, datetime.now().timestamp())
            return False
        elif current_window_req_count >= self.interval_max:
            return True

        self.storage_backend.sorted_set_add(window_key, datetime.now().timestamp())

        return False
