"""Alarm Clock CLI entrypoint."""

from __future__ import annotations

from pathlib import Path

from alarm_clock.scheduler import AlarmScheduler
from alarm_clock.storage import AlarmStore, CorruptedAlarmStoreError

DEFAULT_STORE_PATH = Path(__file__).with_name("alarms.json")

BANNER = """\
==========================
      Alarm Clock
    Time Format: 24 Hour
==========================

1. View Alarms
2. Add Alarm
3. Update Alarm
4. Delete Alarm
5. Exit"""


def _print_alarms(store: AlarmStore) -> None:
    alarms = store.list()
    if not alarms:
        print("No alarms configured.")
        return
    print("ID   Time")
    for alarm in alarms:
        print(f"{alarm['id']:<4} {alarm['time']}")


def _prompt_int(prompt: str) -> int | None:
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("Alarm not found.")
        return None


def run(store_path: Path | None = None) -> int:
    path = store_path or DEFAULT_STORE_PATH
    try:
        store = AlarmStore(path)
    except CorruptedAlarmStoreError as exc:
        print(f"Error: {exc}")
        return 1

    scheduler = AlarmScheduler(on_task_id=store.set_task_id)
    scheduler.restore_all(store.list())

    while True:
        print()
        print(BANNER)
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            _print_alarms(store)

        elif choice == "2":
            time_text = input("Enter alarm time (24-hour): ").strip()
            try:
                alarm = store.add(time_text)
            except ValueError as exc:
                print(exc)
                continue
            scheduler.schedule(alarm)
            print("Alarm added.")

        elif choice == "3":
            alarm_id = _prompt_int("Select alarm: ")
            if alarm_id is None:
                continue
            if store.get(alarm_id) is None:
                print("Alarm not found.")
                continue
            time_text = input("New time: ").strip()
            try:
                updated = store.update(alarm_id, time_text)
            except ValueError as exc:
                print(exc)
                continue
            if updated is None:
                print("Alarm not found.")
                continue
            scheduler.reschedule(updated)
            print("Alarm updated.")

        elif choice == "4":
            alarm_id = _prompt_int("Select alarm to delete: ")
            if alarm_id is None:
                continue
            if store.get(alarm_id) is None:
                print("Alarm not found.")
                continue
            scheduler.cancel(alarm_id)
            store.delete(alarm_id)
            print("Alarm deleted.")

        elif choice == "5":
            scheduler.cancel_all()
            print("Goodbye.")
            return 0

        else:
            print("Invalid option.")


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
