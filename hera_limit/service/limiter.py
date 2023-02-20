from dataclasses import dataclass
from typing import Dict, List, Tuple

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
        self.rule_to_limits: List[Tuple[Rule, List[AbstractStrategy]]] = []
        self.storage_engine = storage_engine

        for rule in rules:
            limits = []
            for descriptor in rule.descriptors:
                if config.limit_strategy == LimitStrategies.TOKEN_BUCKET:
                    limits.append(
                        TokenBucket(
                            storage_backend=self.storage_engine,
                            rule_descriptor=descriptor,
                        )
                    )
                elif config.limit_strategy == LimitStrategies.FIXED_WINDOW:
                    limits.append(
                        TokenBucket(
                            storage_backend=self.storage_engine,
                            rule_descriptor=descriptor,
                        )
                    )
                elif config.limit_strategy == LimitStrategies.SLIDING_WINDOW_LOG:
                    limits.append(
                        TokenBucket(
                            storage_backend=self.storage_engine,
                            rule_descriptor=descriptor,
                        )
                    )
                elif config.limit_strategy == LimitStrategies.SLIDING_WINDOW_COUNTER:
                    limits.append(
                        TokenBucket(
                            storage_backend=self.storage_engine,
                            rule_descriptor=descriptor,
                        )
                    )
                else:
                    raise ValueError(
                        f"Limit strategy {config.limit_strategy} not supported"
                    )

            self.rule_to_limits.append((rule, limits))

    def do_limit(self, request):
        applied_rules = []
        for rule, limits in self.rule_to_limits:
            if rule.match(request.path):
                applied_rules.extend(limits)
        for rule_limits in applied_rules:
            if rule_limits.do_limit(request):
                return True
        return False
