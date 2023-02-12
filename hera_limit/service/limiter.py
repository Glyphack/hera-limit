from typing import Dict, List

from hera_limit.limit_strategy.strategy import LimitStrategies, LimitStrategy
from hera_limit.limit_strategy.token_bucket import TokenBucket
from hera_limit.rules_provider.rule import Rule
from hera_limit.service.config import Config
from hera_limit.storage.memory import Memory
from hera_limit.storage.storage import AbstractStorage, StorageEngines


class RateLimitService:
    def __init__(
        self, config: Config, storage_engine: AbstractStorage, rules: List[Rule]
    ) -> None:
        self.limits_to_check: Dict[str, List[LimitStrategy]] = {}
        self.storage_engine = storage_engine

        for rule in rules:
            self.limits_to_check[rule.path] = []
            for descriptor in rule.descriptors:
                if config.limit_strategy == LimitStrategies.TOKEN_BUCKET:
                    self.limits_to_check[rule.path].append(
                        TokenBucket(
                            storage_backend=self.storage_engine,
                            rule_descriptor=descriptor,
                        )
                    )
                else:
                    raise NotImplementedError

    def do_limit(self, request):
        for limit_to_check in self.limits_to_check.get(request.path, []):
            if limit_to_check.do_limit(request):
                return True
        return False
