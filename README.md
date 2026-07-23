# Alarm Clock CLI

Minimal 24-hour alarm clock for the terminal. Alarms persist in JSON and each
alarm runs on a background timer (no polling loop).

## Requirements

- Python 3.13+
- Audio backend: prefers system `aplay` / `paplay`, then `playsound==1.2.2`
  (1.3.x does not build on Python 3.13; Linux `playsound` also needs `gi`)

## Setup (local)

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt   # pytest
```

On Linux, install ALSA tools so sound works without PyGObject:

```bash
sudo apt install alsa-utils
```

## Run (local)

From the project root:

```bash
python -m alarm_clock
```

## Run (Docker)

Docker bakes in `alsa-utils` and avoids the host `gi` / playsound issue.
Pass `/dev/snd` so the container can play audio on a Linux host.

```bash
docker compose build
docker compose run --rm alarm-clock
```

Alarms persist in [`data/alarms.json`](data/alarms.json) (bind-mounted into the
container). That file must exist before the first run so the volume mount is a
file, not a directory.

Without `/dev/snd` (or on hosts without ALSA), the menu still works but ringing
may fail.

## Menu

1. View Alarms
2. Add Alarm
3. Update Alarm
4. Delete Alarm
5. Exit

Times use 24-hour `HH:MM`. Past times are scheduled for tomorrow. Alarms
repeat daily.

## Tests

```bash
pytest -v
```

## Layout

```
alarm_clock/
  main.py         # CLI menu
  utils.py        # parse_time, next_ring_datetime
  storage.py      # JSON AlarmStore
  scheduler.py    # background Timer per alarm
  audio.py        # ~10s ring (aplay / paplay / playsound)
  alarm.wav
  alarms.json     # created automatically if missing
data/
  alarms.json     # Docker volume seed / persistence
Dockerfile
docker-compose.yml
```
