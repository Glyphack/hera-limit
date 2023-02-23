import datetime

import freezegun
import pytest

from hera_limit.limit_strategy.fixed_window import FixedWindow
from hera_limit.limit_strategy.sliding_window_counter import SlidingWindowCount
from hera_limit.limit_strategy.sliding_window_log import SlidingWindowLog
from hera_limit.limit_strategy.strategy import Request
from hera_limit.limit_strategy.token_bucket import TokenBucket
from hera_limit.rules_provider.rule import Descriptor, Unit
from hera_limit.storage import memory


@pytest.fixture
def local_storage():
    local_storage = memory.Memory()
    yield local_storage
    local_storage.data = {}


@pytest.mark.parametrize(
    "limit_strategy",
    [
        TokenBucket,
        FixedWindow,
        SlidingWindowLog,
        SlidingWindowCount,
    ],
)
def test_apply_limit_per_unit(local_storage, limit_strategy):
    rule_descriptor = Descriptor(
        key="user_id",
        requests_per_unit=1,
        unit=Unit.SECOND,
    )
    token_bucket = limit_strategy(
        storage_backend=local_storage,
        rule_descriptor=rule_descriptor,
    )
    request = Request(path="dd", data={"user_id": "1"})
    assert token_bucket.do_limit(request) is False
    assert token_bucket.do_limit(request) is True

    test_now = datetime.datetime.now() + datetime.timedelta(seconds=3)
    with freezegun.freeze_time(test_now):
        assert token_bucket.do_limit(request) is False


@pytest.mark.parametrize(
    "limit_strategy",
    [
        TokenBucket,
        FixedWindow,
        SlidingWindowLog,
        SlidingWindowCount,
    ],
)
def test_apply_limit_per_value(local_storage, limit_strategy):
    rule_descriptor = Descriptor(
        key="user_id",
        requests_per_unit=1,
        unit=Unit.SECOND,
    )
    token_bucket = limit_strategy(
        storage_backend=local_storage,
        rule_descriptor=rule_descriptor,
    )
    user_1_request = Request(path="dd", data={"user_id": "1"})
    user_2_request = Request(path="dd", data={"user_id": "2"})

    assert token_bucket.do_limit(user_1_request) is False
    assert token_bucket.do_limit(user_2_request) is False
    assert token_bucket.do_limit(user_1_request) is True
    assert token_bucket.do_limit(user_2_request) is True


@pytest.mark.parametrize(
    "limit_strategy",
    [
        TokenBucket,
        FixedWindow,
        SlidingWindowLog,
        SlidingWindowCount,
    ],
)
def test_apply_limit_specific_value(local_storage, limit_strategy):
    rule_descriptor = Descriptor(
        key="user_id",
        value="1",
        requests_per_unit=1,
        unit=Unit.MINUTE,
    )
    token_bucket = limit_strategy(
        storage_backend=local_storage,
        rule_descriptor=rule_descriptor,
    )
    user_1_req = Request(path="dd", data={"user_id": "1"})
    user_2_req = Request(path="dd", data={"user_id": "2"})

    assert token_bucket.do_limit(user_1_req) is False
    assert token_bucket.do_limit(user_2_req) is False
    assert token_bucket.do_limit(user_1_req) is True


@pytest.mark.parametrize(
    "limit_strategy",
    [
        SlidingWindowLog,
        SlidingWindowCount,
    ],
)
def test_sliding_window_does_not_allow_requests_in_unit_edges(
    local_storage, limit_strategy
):
    rule_descriptor = Descriptor(
        key="user_id",
        requests_per_unit=2,
        unit=Unit.MINUTE,
    )
    sliding_window = limit_strategy(
        storage_backend=local_storage,
        rule_descriptor=rule_descriptor,
    )
    user_1_req = Request(path="dd", data={"user_id": "1"})

    current_time = datetime.datetime.now().replace(
        hour=0, minute=0, second=50, microsecond=0
    )
    with freezegun.freeze_time(current_time):
        assert sliding_window.do_limit(user_1_req) is False

    test_now = current_time + datetime.timedelta(seconds=15)
    with freezegun.freeze_time(test_now):
        assert sliding_window.do_limit(user_1_req) is False
        assert sliding_window.do_limit(user_1_req) is True
