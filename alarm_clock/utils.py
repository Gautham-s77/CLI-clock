"""Time parsing and next-ring helpers for the alarm clock."""

from __future__ import annotations

import re
from datetime import datetime, timedelta

_TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")

_INVALID_TIME_MSG = "Invalid time.\nUse HH:MM (24-hour)."


def parse_time(text: str) -> tuple[int, int]:
    """Parse a 24-hour HH:MM string into (hour, minute).

    Raises:
        ValueError: If the text is not a valid 24-hour time.
    """
    if not isinstance(text, str):
        raise ValueError(_INVALID_TIME_MSG)

    match = _TIME_RE.fullmatch(text.strip())
    if match is None:
        raise ValueError(_INVALID_TIME_MSG)

    hour = int(match.group(1))
    minute = int(match.group(2))
    return hour, minute


def next_ring_datetime(hhmm: str, *, now: datetime) -> datetime:
    """Return the next datetime when an HH:MM alarm should ring.

    If the candidate time for today is less than or equal to ``now``,
    the alarm is scheduled for tomorrow.
    """
    hour, minute = parse_time(hhmm)
    candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate <= now:
        candidate += timedelta(days=1)
    return candidate
