from pydantic import BaseSettings

from hera_limit.limit_strategy.strategy import LimitStrategies

class Config(BaseSettings):
    limit_strategy: LimitStrategies
