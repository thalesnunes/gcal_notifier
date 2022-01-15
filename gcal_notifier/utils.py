import os
import shlex
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import NoReturn

import simpleaudio as sa

ROOT_DIR = Path(__file__).parent
CONFIG = Path(os.path.expanduser("~/.config/gcal_notifier"))
GENERAL_PARAMS = {
    "time_min": datetime.now(),
    "time_max": datetime.now() + timedelta(days=1),
    "order_by": "startTime",
    "single_events": True,
}
CMD = "notify-send -u critical -a GoogleCalendar {calendar} {title}"


def validate_sound_file(wav_file: str) -> bool:
    """Asserts if sound file is valid.

    Args:
        wav_file (str): Path to wav file

    Returns:
        bool: If file is valid
    """
    return wav_file.endswith(".wav")


def make_sound(
        sound_path: Path = ROOT_DIR / "resources" / "pop.wav"
) -> NoReturn:
    """Play sound in sound_path.

    Args:
        sound_path (Path): Path to a wav sound file
    """
    sound_file = str(sound_path.absolute())
    if validate_sound_file(sound_file):
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        wave_obj.play()


def run_notify(command: str = CMD) -> NoReturn:
    """Run notification command.

    Args:
        command (str): Command to be run
    """
    subprocess.run(shlex.split(command))
    # TODO: implement configurable notification sound
    make_sound()
