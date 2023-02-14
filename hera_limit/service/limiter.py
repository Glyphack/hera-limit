from dataclasses import dataclass
from typing import Dict, List

from hera_limit.limit_strategy.strategy import (
    AbstractStrategy,
    LimitStrategies,
)
from hera_limit.limit_strategy.token_bucket import TokenBucket
from hera_limit.rules_provider.rule import Rule
from hera_limit.storage.storage import AbstractStorage


@dataclass
class Config:
    limit_strategy: LimitStrategies


class RateLimitService:
    def __init__(
        self, config: Config, storage_engine: AbstractStorage, rules: List[Rule]
    ) -> None:
        self.rule_to_limits: Dict[Rule, List[AbstractStrategy]] = {}
        self.storage_engine = storage_engine

        for rule in rules:
            self.rule_to_limits[rule] = []
            for descriptor in rule.descriptors:
                if config.limit_strategy == LimitStrategies.TOKEN_BUCKET:
                    self.rule_to_limits[rule].append(
                        TokenBucket(
                            storage_backend=self.storage_engine,
                            rule_descriptor=descriptor,
                        )
                    )
                else:
                    raise NotImplementedError

    def do_limit(self, request):
        applied_rules = []
        for rule, limits in self.rule_to_limits.items():
            if rule.match(request.path):
                applied_rules.append(limits)
        for rule_limits in applied_rules:
            if rule_limits.do_limit(request):
                return True
        return False
