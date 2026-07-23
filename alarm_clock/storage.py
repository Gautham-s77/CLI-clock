"""JSON-backed persistence for alarms."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from alarm_clock.utils import parse_time


class CorruptedAlarmStoreError(Exception):
    """Raised when the alarm JSON file cannot be parsed."""


class AlarmStore:
    """Load and persist alarms in a local JSON file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._alarms: list[dict[str, Any]] = self._load()

    def _load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("[]\n", encoding="utf-8")
            return []
        try:
            raw = self.path.read_text(encoding="utf-8")
            if not raw.strip():
                return []
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            raise CorruptedAlarmStoreError(
                f"Could not parse alarm storage file: {self.path}"
            ) from exc

        if not isinstance(data, list):
            raise CorruptedAlarmStoreError(
                f"Alarm storage must be a JSON list: {self.path}"
            )
        return data

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._alarms, indent=4) + "\n",
            encoding="utf-8",
        )

    def _next_id(self) -> int:
        if not self._alarms:
            return 1
        return max(int(alarm["id"]) for alarm in self._alarms) + 1

    def list(self) -> list[dict[str, Any]]:
        return list(self._alarms)

    def get(self, alarm_id: int) -> dict[str, Any] | None:
        for alarm in self._alarms:
            if int(alarm["id"]) == int(alarm_id):
                return alarm
        return None

    def add(self, time: str) -> dict[str, Any]:
        hour, minute = parse_time(time)
        normalized = f"{hour:02d}:{minute:02d}"
        alarm: dict[str, Any] = {
            "id": self._next_id(),
            "time": normalized,
            "task_id": None,
        }
        self._alarms.append(alarm)
        self._save()
        return dict(alarm)

    def update(self, alarm_id: int, time: str) -> dict[str, Any] | None:
        alarm = self.get(alarm_id)
        if alarm is None:
            return None
        hour, minute = parse_time(time)
        alarm["time"] = f"{hour:02d}:{minute:02d}"
        self._save()
        return dict(alarm)

    def delete(self, alarm_id: int) -> bool:
        for index, alarm in enumerate(self._alarms):
            if int(alarm["id"]) == int(alarm_id):
                del self._alarms[index]
                self._save()
                return True
        return False

    def set_task_id(self, alarm_id: int, task_id: int | None) -> None:
        alarm = self.get(alarm_id)
        if alarm is None:
            return
        alarm["task_id"] = task_id
        self._save()
