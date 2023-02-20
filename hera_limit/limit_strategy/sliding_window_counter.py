from datetime import datetime
from os import preadv

from hera_limit.limit_strategy.strategy import AbstractStrategy, Request
from hera_limit.rules_provider.rule import Descriptor
from hera_limit.storage.storage import AbstractStorage


class SlidingWindowCount(AbstractStrategy):
    def __init__(
        self,
        storage_backend: AbstractStorage,
        rule_descriptor: Descriptor,
    ):
        super(SlidingWindowCount, self).__init__(storage_backend, rule_descriptor)
        self.interval_len_sec = self.rule_descriptor.unit.to_seconds()
        self.interval_max = self.rule_descriptor.requests_per_unit

    def do_limit(self, request: Request):
        current_interval = str(datetime.now().timestamp() // self.interval_len_sec)
        prev_interval = str(datetime.now().timestamp() // self.interval_len_sec - 1)
        key = self.rule_descriptor.key
        path = request.path
        value = request.data[key]

        previous_interval_key = self._get_counter_key(prev_interval, path, key, value)
        current_interval_key = self._get_counter_key(current_interval, path, key, value)

        previous_interval_counter = self.storage_backend.get(previous_interval_key) or 0
        current_interval_counter = self.storage_backend.get(current_interval_key) or 0

        percent_of_current_interval_remaining = (
            self.interval_len_sec - datetime.now().timestamp() % self.interval_len_sec
        ) / self.interval_len_sec
        percent_of_current_interval_passed = 1 - percent_of_current_interval_remaining

        total_requests = (
            previous_interval_counter
            + current_interval_counter * percent_of_current_interval_passed
        )

        if total_requests >= self.interval_max:
            return True

        return False

    def _get_counter_key(self, interval, path, key, value):
        descriptor = self.rule_descriptor
        key = descriptor.key
        if descriptor.value is not None and value != descriptor.value:
            return None
        else:
            return path + interval + "_" + key + "_" + value
