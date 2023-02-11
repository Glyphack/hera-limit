from pathlib import Path
from typing import Dict, List

from hera_limit.limit_strategy.strategy import LimitStrategies, LimitStrategy
from hera_limit.limit_strategy.token_bucket import TokenBucket
from hera_limit.rules_provider import file_provider
from hera_limit.rules_provider.rule import Unit
from hera_limit.service.config import Config
from hera_limit.storage.memory import Memory
from hera_limit.storage.storage import StorageEngines


class RateLimitService:
    def __init__(self, config: Config) -> None:
        if config.storage_engine == StorageEngines.MEMORY:
            self.storage_engine = Memory()
        else:
            raise NotImplementedError

        rules = file_provider.load_rules(Path(config.rules_path))
        self.limits_to_check: Dict[str, List[LimitStrategy]] = {}

        for rule in rules:
            self.limits_to_check[rule.path] = []
            for descriptor in rule.descriptors:
                if config.limit_strategy == LimitStrategies.TOKEN_BUCKET:
                    if descriptor.unit == Unit.SECOND:
                        refill_period = 1
                    elif descriptor.unit == Unit.MINUTE:
                        refill_period = 60
                    elif descriptor.unit == Unit.HOUR:
                        refill_period = 3600
                    else:
                        refill_period = 1
                    self.limits_to_check[rule.path].append(
                        TokenBucket(
                            storage_backend=self.storage_engine,
                            rule_descriptor=descriptor,
                            refill_every_x_seconds=refill_period,
                            capacity=descriptor.requests_per_unit,
                        )
                    )
                else:
                    raise NotImplementedError

    def do_limit(self, request):
        for limit_to_check in self.limits_to_check[request.path]:
            if limit_to_check.do_limit(request):
                return True
