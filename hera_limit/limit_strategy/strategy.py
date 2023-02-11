import abc
from dataclasses import dataclass
from enum import Enum

from hera_limit.rules_provider.rule import Descriptor
from hera_limit.storage.storage import AbstractStorage


class LimitStrategies(str, Enum):
    TOKEN_BUCKET = "token_bucket"


@dataclass
class Request:
    path: str
    data: dict


class LimitStrategy(abc.ABC, metaclass=abc.ABCMeta):
    def __init__(
        self,
        storage_backend: AbstractStorage,
        rule_descriptor: Descriptor,
    ) -> None:

        self.storage_backend = storage_backend
        self.rule_descriptor = rule_descriptor

    def do_limit(
        self,
        request: Request,
    ):
        raise NotImplementedError
