import datetime
from unittest import mock

import freezegun
import pytest

from hera_limit.limit_strategy.strategy import LimitStrategies, Request
from hera_limit.rules_provider.rule import Descriptor, Rule, Unit
from hera_limit.service.limiter import Config, RateLimitService
from hera_limit.storage import memory


@pytest.fixture
def local_storage():
    local_storage = memory.Memory()
    yield local_storage
    local_storage.data = {}


@pytest.fixture
def config():
    return Config(
        limit_strategy=LimitStrategies.TOKEN_BUCKET,
    )


def test_rate_limit_service_limits_requests(
    local_storage: memory.Memory, config: Config
):
    rule_descriptor = Descriptor(
        key="user_id",
        requests_per_unit=1,
        unit=Unit.SECOND,
    )
    rule = Rule(path="/limited-path", descriptors=[rule_descriptor])
    rate_limit_service = RateLimitService(
        config=config, storage_engine=local_storage, rules=[rule]
    )
    request = Request(path="/limited-path", data={"user_id": "1"})
    assert rate_limit_service.do_limit(request) is False
    assert rate_limit_service.do_limit(request) is True

    time_now = datetime.datetime.now() + datetime.timedelta(seconds=3)
    with freezegun.freeze_time(time_now):
        assert rate_limit_service.do_limit(request) is False
