import abc
from dataclasses import dataclass

from hera_limit.rules_provider.rule import Rule
from hera_limit.storage.storage import AbstractStorage


@dataclass
class Request:
    data: dict


class AbstractStrategy(abc.ABC):
    def __init__(
        self, storage_backend: AbstractStorage, rule: Rule, request: Request
    ) -> None:
        super().__init__()

        self.storage_backend = storage_backend
        self.rule = rule
        self.request = request

    def do_limit(
        self,
    ):
        raise NotImplementedError
