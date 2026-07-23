"""Alarm sound playback (~10 seconds)."""

from __future__ import annotations

import shutil
import subprocess
import threading
import time
from pathlib import Path

SOUND_PATH = Path(__file__).with_name("alarm.wav")


def _play_once(path: Path) -> None:
    """Play the sound file once using the best available backend."""
    aplay = shutil.which("aplay")
    if aplay is not None:
        subprocess.run([aplay, "-q", str(path)], check=False)
        return

    paplay = shutil.which("paplay")
    if paplay is not None:
        subprocess.run([paplay, str(path)], check=False)
        return

    try:
        from playsound import playsound
    except ImportError as exc:
        raise RuntimeError(
            "No audio backend found (aplay/paplay/playsound)."
        ) from exc

    playsound(str(path), block=True)


def ring(duration_seconds: float = 10.0, sound_path: Path | None = None) -> None:
    """Play the bundled alarm sound for approximately ``duration_seconds``.

    Prefers ALSA ``aplay``, then PulseAudio ``paplay``, then ``playsound``.
    Playback runs in a daemon thread; the short WAV is looped until the
    duration elapses.
    """
    path = Path(sound_path) if sound_path is not None else SOUND_PATH
    if not path.exists():
        print(f"Alarm sound not found: {path}")
        return

    stop_at = time.monotonic() + duration_seconds
    done = threading.Event()

    def _play_loop() -> None:
        try:
            while time.monotonic() < stop_at and not done.is_set():
                _play_once(path)
        except Exception as exc:  # noqa: BLE001 - audio backends vary by OS
            print(f"Alarm audio error: {exc}")
        finally:
            done.set()

    thread = threading.Thread(target=_play_loop, name="alarm-ring", daemon=True)
    thread.start()
    thread.join(timeout=duration_seconds + 2.0)
    done.set()
