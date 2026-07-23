"""Background timers that fire alarms without polling."""

from __future__ import annotations

import threading
from datetime import datetime
from typing import Any, Callable

from alarm_clock import audio
from alarm_clock.utils import next_ring_datetime


class AlarmScheduler:
    """Schedule one ``threading.Timer`` per alarm; cancel/reschedule by id."""

    def __init__(
        self,
        *,
        on_task_id: Callable[[int, int | None], None] | None = None,
        ring: Callable[[], None] | None = None,
    ) -> None:
        self._timers: dict[int, threading.Timer] = {}
        self._task_seq = 0
        self._lock = threading.Lock()
        self._on_task_id = on_task_id
        self._ring = ring or (lambda: audio.ring())

    def _next_task_id(self) -> int:
        self._task_seq += 1
        return self._task_seq

    def cancel(self, alarm_id: int) -> None:
        with self._lock:
            timer = self._timers.pop(int(alarm_id), None)
        if timer is not None:
            timer.cancel()
        if self._on_task_id is not None:
            self._on_task_id(int(alarm_id), None)

    def cancel_all(self) -> None:
        with self._lock:
            alarm_ids = list(self._timers.keys())
        for alarm_id in alarm_ids:
            self.cancel(alarm_id)

    def schedule(self, alarm: dict[str, Any], *, now: datetime | None = None) -> int:
        """Schedule ``alarm`` to ring at the next occurrence of its time."""
        alarm_id = int(alarm["id"])
        self.cancel(alarm_id)

        when = next_ring_datetime(alarm["time"], now=now or datetime.now())
        delay = max(0.0, (when - (now or datetime.now())).total_seconds())
        task_id = self._next_task_id()

        def _fire() -> None:
            with self._lock:
                self._timers.pop(alarm_id, None)
            print(f"\n*** Alarm {alarm_id} ({alarm['time']}) ***")
            self._ring()
            # Daily repeat: schedule again for the next day.
            self.schedule(alarm)

        timer = threading.Timer(delay, _fire)
        timer.daemon = True
        with self._lock:
            self._timers[alarm_id] = timer
        timer.start()

        if self._on_task_id is not None:
            self._on_task_id(alarm_id, task_id)
        return task_id

    def reschedule(self, alarm: dict[str, Any], *, now: datetime | None = None) -> int:
        return self.schedule(alarm, now=now)

    def restore_all(
        self,
        alarms: list[dict[str, Any]],
        *,
        now: datetime | None = None,
    ) -> None:
        for alarm in alarms:
            self.schedule(alarm, now=now)
