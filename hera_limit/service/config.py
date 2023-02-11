from pydantic import BaseSettings

from hera_limit.limit_strategy.strategy import LimitStrategies
from hera_limit.storage.storage import StorageEngines


class Config(BaseSettings):
    storage_engine: StorageEngines
    limit_strategy: LimitStrategies
    rules_path: str
