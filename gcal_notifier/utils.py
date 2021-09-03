from datetime import datetime, timedelta
import os
from pathlib import Path
import shlex
import subprocess

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
    return wav_file.endswith(".wav")


def make_sound(sound_path: Path = ROOT_DIR / "resources" / "pop.wav"):
    sound_file = str(sound_path.absolute())
    if validate_sound_file(sound_file):
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        wave_obj.play()


def run_notify(command: str = CMD):
    subprocess.run(shlex.split(command))
    # TODO: implement configurable notification sound
    make_sound()
