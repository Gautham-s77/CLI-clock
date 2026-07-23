"""Tests for valid alarm creation via AlarmStore.add."""

import json

import pytest

from alarm_clock.storage import AlarmStore


def test_add_alarm_persists_to_json(tmp_path):
    path = tmp_path / "alarms.json"
    store = AlarmStore(path)

    alarm = store.add("18:45")

    assert alarm["time"] == "18:45"
    assert isinstance(alarm["id"], int)

    data = json.loads(path.read_text())
    assert len(data) == 1
    assert data[0]["id"] == alarm["id"]
    assert data[0]["time"] == "18:45"


def test_add_two_alarms_distinct_ids(tmp_path):
    path = tmp_path / "alarms.json"
    store = AlarmStore(path)

    first = store.add("07:30")
    second = store.add("22:00")

    assert first["id"] != second["id"]

    data = json.loads(path.read_text())
    assert len(data) == 2
    times = {entry["time"] for entry in data}
    assert times == {"07:30", "22:00"}


def test_add_duplicate_times_allowed(tmp_path):
    path = tmp_path / "alarms.json"
    store = AlarmStore(path)

    first = store.add("08:00")
    second = store.add("08:00")

    assert first["id"] != second["id"]
    assert first["time"] == second["time"] == "08:00"

    data = json.loads(path.read_text())
    assert len(data) == 2
    assert all(entry["time"] == "08:00" for entry in data)


def test_add_rejects_invalid_time(tmp_path):
    path = tmp_path / "alarms.json"
    store = AlarmStore(path)

    with pytest.raises(ValueError) as exc_info:
        store.add("25:00")

    message = str(exc_info.value)
    assert "Invalid time" in message
    assert "HH:MM" in message
    assert not path.exists() or json.loads(path.read_text()) == []
