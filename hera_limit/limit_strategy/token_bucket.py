from strategy import LimitStrategy

from hera_limit.limit_strategy.strategy import Request


class TokenBucket(LimitStrategy):
    def __init__(self, refill_every_x_seconds: int, capacity: int, **kwargs):
        super(TokenBucket, self).__init__(**kwargs)
        self.capacity = capacity
        self.refill_every_x_seconds = refill_every_x_seconds

    def do_limit(self, request: Request):
        self.request = request
        counter_key = self.get_counter_keys()
        if counter_key is None:
            return False
        if self.consume(counter_key):
            return False

        return True

    def get_counter_keys(self):
        descriptor = self.rule_descriptor
        path = self.request.path
        key = descriptor.key
        value = self.request.data[key]
        if descriptor.value is not None and value != descriptor.value:
            return None
        else:
            return path + "_" + key + "_" + value

    def consume(self, counter_key):
        counter = self.storage_backend.get(counter_key)
        if counter is None:
            counter = self.capacity
        elif counter <= 0:
            return False

        counter -= 1
        self.storage_backend.set(counter_key, counter, self.refill_every_x_seconds)

        return True
