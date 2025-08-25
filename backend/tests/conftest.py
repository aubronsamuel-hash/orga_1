import os

import pytest

os.environ.setdefault("RATE_LIMIT_TEST_PREFIX", "test:")
os.environ.setdefault("RATE_LIMIT_LOGIN_PER_MIN", "100")
os.environ.setdefault("RATE_LIMIT_WINDOW_SEC", "10")


@pytest.fixture(autouse=True)
def _reset_rl():
    from app.rate_limit import clear_test_keys

    clear_test_keys()
    yield
    clear_test_keys()
