import abc
from dataclasses import dataclass
from enum import Enum

from hera_limit.rules_provider.rule import Descriptor
from hera_limit.storage.storage import AbstractStorage


class LimitStrategies(str, Enum):
    TOKEN_BUCKET = "token_bucket"
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW_LOG = "sliding_window_log"
    SLIDING_WINDOW_COUNTER = "sliding_window_counter"


@dataclass
class Request:
    path: str
    data: dict


class AbstractStrategy(abc.ABC, metaclass=abc.ABCMeta):
    def __init__(
        self,
        storage_backend: AbstractStorage,
        rule_descriptor: Descriptor,
    ) -> None:
        self.storage_backend = storage_backend
        self.rule_descriptor = rule_descriptor

    @abc.abstractmethod
    def do_limit(
        self,
        request: Request,
    ):
        raise NotImplementedError
