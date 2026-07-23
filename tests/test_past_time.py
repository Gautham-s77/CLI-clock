"""Tests for past-time → tomorrow scheduling (next_ring_datetime)."""

from datetime import datetime

from alarm_clock.utils import next_ring_datetime


NOW = datetime(2026, 7, 24, 18, 0)


def test_past_time_schedules_tomorrow():
    result = next_ring_datetime("17:30", now=NOW)
    assert result == datetime(2026, 7, 25, 17, 30)


def test_future_time_schedules_today():
    result = next_ring_datetime("18:45", now=NOW)
    assert result == datetime(2026, 7, 24, 18, 45)


def test_exact_current_minute_schedules_tomorrow():
    result = next_ring_datetime("18:00", now=NOW)
    assert result == datetime(2026, 7, 25, 18, 0)
