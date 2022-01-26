import calendar
import shlex
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

import simpleaudio as sa

from gcal_notifier.globals import CMD, ROOT_DIR


def is_sound_valid(wav_file: str) -> bool:
    """Asserts if sound file is valid.

    Args:
        wav_file (str): Path to wav file

    Returns:
        bool: If file is valid
    """
    return wav_file.endswith(".wav")


def make_sound(
    sound_path: Path = ROOT_DIR / "resources" / "pop.wav",
) -> None:
    """Play sound in sound_path.

    Args:
        sound_path (Path): Path to a wav sound file

    Raises:
        Exception: Wrong sound file extension
    """
    sound_file = str(sound_path.absolute())
    if is_sound_valid(sound_file):
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    else:
        raise Exception("The given sound file is not valid. It must be a .wav")


def run_notify(
    command: str = CMD,
    sound_path: Path = ROOT_DIR / "resources" / "pop.wav",
) -> None:
    """Run notification command.

    Args:
        command (str): Command to be run
        sound_path (Path): Path to a wav sound file
    """
    subprocess.run(shlex.split(command))
    make_sound(sound_path)


def define_period(period: str = "day") -> Tuple[datetime, datetime]:
    """Define period based on string.

    Args:
        period (str): Period as string: "week", "month", "day"

    Returns:
        Tuple[datetime, datetime]: (Start datetime, End datetime)
    """
    today = datetime.now()

    if period.startswith("d"):
        time_min = today
        time_max = today + timedelta(days=1)

    elif period.startswith("w"):
        weekday = today.weekday()
        time_min = today - timedelta(days=weekday + 1)
        to_sum = 5 - weekday if weekday != 6 else 6
        time_max = today + timedelta(days=to_sum)

    elif period.startswith("m"):
        time_min = today.replace(day=1)
        time_max = today.replace(
            day=calendar.monthrange(today.year, today.month)[1]
        )

    return time_min, time_max
