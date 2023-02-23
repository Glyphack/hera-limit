import math
from datetime import datetime

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
        current_interval = str(int(datetime.now().timestamp() / self.interval_len_sec))
        prev_interval = str(int(datetime.now().timestamp() / self.interval_len_sec) - 1)
        key = self.rule_descriptor.key
        path = request.path
        value = request.data[key]

        previous_interval_key = self._get_counter_key(prev_interval, path, key, value)
        current_interval_key = self._get_counter_key(current_interval, path, key, value)

        if previous_interval_key is None or current_interval_key is None:
            return False

        self.storage_backend.incr(current_interval_key)

        current_interval_counter = self.storage_backend.get(current_interval_key) or 0
        previous_interval_counter = self.storage_backend.get(previous_interval_key) or 0

        percent_of_previous_interval_overlap_current_window = (
            1
            - (
                self.interval_len_sec
                - datetime.now().timestamp() % self.interval_len_sec
            )
            / self.interval_len_sec
        )

        total_requests = math.ceil(
            previous_interval_counter
            * percent_of_previous_interval_overlap_current_window
            + current_interval_counter
        )

        if total_requests > self.interval_max:
            return True

        return False

    def _get_counter_key(self, interval, path, key, value):
        descriptor = self.rule_descriptor
        key = descriptor.key
        if descriptor.value is not None and value != descriptor.value:
            return None
        else:
            return path + interval + "_" + key + "_" + value
