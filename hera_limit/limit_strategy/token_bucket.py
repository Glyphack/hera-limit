from hera_limit.limit_strategy.strategy import AbstractStrategy, Request
from hera_limit.rules_provider.rule import Descriptor, Unit
from hera_limit.storage.storage import AbstractStorage


class TokenBucket(AbstractStrategy):
    def __init__(
        self,
        storage_backend: AbstractStorage,
        rule_descriptor: Descriptor,
    ):
        super(TokenBucket, self).__init__(storage_backend, rule_descriptor)
        unit = self.rule_descriptor.unit
        if unit == Unit.SECOND:
            refill_period = 1
        elif unit == Unit.MINUTE:
            refill_period = 60
        elif unit == Unit.HOUR:
            refill_period = 3600
        else:
            refill_period = 1
        self.capacity = self.rule_descriptor.requests_per_unit
        self.refill_every_x_seconds = refill_period

    def do_limit(self, request: Request):
        self.request = request
        counter_key = self._get_counter_key()
        if counter_key is None:
            return False
        if self._consume(counter_key):
            return False

        return True

    def _get_counter_key(self):
        descriptor = self.rule_descriptor
        path = self.request.path
        key = descriptor.key
        value = self.request.data[key]
        if descriptor.value is not None and value != descriptor.value:
            return None
        else:
            return path + "_" + key + "_" + value

    def _consume(self, counter_key):
        counter = self.storage_backend.get(counter_key)
        if counter is None:
            counter = self.capacity
        elif counter <= 0:
            return False

        counter -= 1
        self.storage_backend.set(counter_key, counter, self.refill_every_x_seconds)

        return True
