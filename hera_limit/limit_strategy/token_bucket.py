from strategy import AbstractStrategy


class TokenBucket(AbstractStrategy):
    def __init__(self, refill_every_x_seconds: int, capacity: int, **kwargs):
        super(TokenBucket, self).__init__(**kwargs)
        self.capacity = capacity
        self.refill_every_x_seconds = refill_every_x_seconds

    def do_limit(self):
        counter_keys = self.get_counter_keys()
        for counter_key in counter_keys:
            if self.consume(counter_key):
                return False

    def get_counter_keys(self):
        descriptors = self.rule.descriptors
        for descriptor in descriptors:
            key = descriptor.key
            value = self.request.data[key]
            if descriptor.value is not None and value != descriptor.value:
                continue
            yield self.rule.path + "_" + key + "_" + value

    def consume(self, counter_key):
        counter = self.storage_backend.get(counter_key)
        if counter is None:
            counter = self.capacity
        elif counter <= 0:
            return False

        counter -= 1
        self.storage_backend.set(counter_key, counter, self.refill_every_x_seconds)

        return True
