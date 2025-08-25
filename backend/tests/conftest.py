import os

import pytest

os.environ.setdefault("RATE_LIMIT_TEST_PREFIX", "test:")

@pytest.fixture(autouse=True)
def reset_rate_limits():
    from app.rate_limit import clear_rate_limit_test_keys
    clear_rate_limit_test_keys()
    yield
    clear_rate_limit_test_keys()
