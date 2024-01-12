import pytest
from karpatkit.constants import Constants


class TestingConstants(Constants):
    a = "leter_a"
    B = "leter_B"


def test_constant_is_read_only():
    with pytest.raises(AttributeError):
        TestingConstants.a = "other_value"


def test_constant_value_is_str():
    assert TestingConstants.a == "leter_a"
    assert TestingConstants.B == "leter_B"
    assert isinstance(TestingConstants.a, str)
    assert isinstance(TestingConstants.B, str)
