import datetime
from unittest import mock

import pytest

from hera_limit.limit_strategy.strategy import Request
from hera_limit.limit_strategy.token_bucket import TokenBucket
from hera_limit.rules_provider.rule import Descriptor, Unit
from hera_limit.storage import memory


@pytest.fixture
def local_storage():
    yield memory.Memory()


def test_token_bucket_apply_limit_per_unit(local_storage):
    rule_descriptor = Descriptor(
        key="user_id",
        requests_per_unit=1,
        unit=Unit.SECOND,
    )
    token_bucket = TokenBucket(
        storage_backend=local_storage,
        rule_descriptor=rule_descriptor,
    )
    request = Request(path="dd", data={"user_id": "1"})
    assert token_bucket.do_limit(request) is False
    # next request should be limited
    assert token_bucket.do_limit(request) is True

    local_storage.current_time = mock.MagicMock(
        return_value=datetime.datetime.now() + datetime.timedelta(seconds=2)
    )
    assert token_bucket.do_limit(request) is False


def test_token_bucket_apply_limit_for_values(local_storage):
    rule_descriptor = Descriptor(
        key="user_id",
        requests_per_unit=1,
        unit=Unit.SECOND,
    )
    token_bucket = TokenBucket(
        storage_backend=local_storage,
        rule_descriptor=rule_descriptor,
    )
    user_1_request = Request(path="dd", data={"user_id": "1"})
    user_2_request = Request(path="dd", data={"user_id": "2"})

    assert token_bucket.do_limit(user_1_request) is False
    assert token_bucket.do_limit(user_2_request) is False
    # next request should be limited
    assert token_bucket.do_limit(user_1_request) is True
    assert token_bucket.do_limit(user_2_request) is True


def test_token_bucket_apply_limit_specific_values(local_storage):
    rule_descriptor = Descriptor(
        key="user_id",
        value="1",
        requests_per_unit=1,
        unit=Unit.MINUTE,
    )
    token_bucket = TokenBucket(
        storage_backend=local_storage,
        rule_descriptor=rule_descriptor,
    )
    user_1_req = Request(path="dd", data={"user_id": "1"})
    user_2_req = Request(path="dd", data={"user_id": "2"})

    assert token_bucket.do_limit(user_1_req) is False
    assert token_bucket.do_limit(user_2_req) is False
    # next request should be limited
    assert token_bucket.do_limit(user_1_req) is True
