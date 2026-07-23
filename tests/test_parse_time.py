"""Tests for HH:MM time parsing (alarm_clock.utils.parse_time)."""

import pytest

from alarm_clock.utils import parse_time


@pytest.mark.parametrize(
    "text,expected",
    [
        ("00:00", (0, 0)),
        ("07:30", (7, 30)),
        ("18:45", (18, 45)),
        ("23:59", (23, 59)),
    ],
)
def test_parse_time_valid(text, expected):
    assert parse_time(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        "25:00",
        "12:60",
        "abc",
        "7pm",
        "18-30",
    ],
)
def test_parse_time_invalid(text):
    with pytest.raises(ValueError) as exc_info:
        parse_time(text)

    message = str(exc_info.value)
    assert "Invalid time" in message
    assert "HH:MM" in message
