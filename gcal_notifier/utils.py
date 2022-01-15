import os
import shlex
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

import simpleaudio as sa

ROOT_DIR = Path(__file__).parent
CONFIG = Path(os.path.expanduser("~/.config/gcal_notifier"))
GENERAL_PARAMS = {
    "time_min": datetime.now().replace(
                                    day=1,
                                    hour=0,
                                    minute=0,
                                    second=0,
                                    microsecond=0
                                ),
    "time_max": datetime.now() + timedelta(days=1),
    "order_by": "startTime",
    "single_events": True,
}
CMD = "notify-send -u critical -a GoogleCalendar {calendar} {title}"
COLORS = {
        'default': '\033[0m',
        'black': '\033[0;30m',
        'brightblack': '\033[30;1m',
        'red': '\033[0;31m',
        'brightred': '\033[31;1m',
        'green': '\033[0;32m',
        'brightgreen': '\033[32;1m',
        'yellow': '\033[0;33m',
        'brightyellow': '\033[33;1m',
        'blue': '\033[0;34m',
        'brightblue': '\033[34;1m',
        'magenta': '\033[0;35m',
        'brightmagenta': '\033[35;1m',
        'cyan': '\033[0;36m',
        'brightcyan': '\033[36;1m',
        'white': '\033[0;37m',
        'brightwhite': '\033[37;1m',
        None: '\033[0m'}

ART_CHARS = {
    'fancy': {
        'hrz': '\033(0\x71\033(B',
        'vrt': '\033(0\x78\033(B',
        'lrc': '\033(0\x6A\033(B',
        'urc': '\033(0\x6B\033(B',
        'ulc': '\033(0\x6C\033(B',
        'llc': '\033(0\x6D\033(B',
        'crs': '\033(0\x6E\033(B',
        'lte': '\033(0\x74\033(B',
        'rte': '\033(0\x75\033(B',
        'bte': '\033(0\x76\033(B',
        'ute': '\033(0\x77\033(B'
        },
    'ascii': {
        'hrz': '-',
        'vrt': '|',
        'lrc': '+',
        'urc': '+',
        'ulc': '+',
        'llc': '+',
        'crs': '+',
        'lte': '+',
        'rte': '+',
        'bte': '+',
        'ute': '+'
        }
    }


def validate_sound_file(wav_file: str) -> bool:
    """Asserts if sound file is valid.

    Args:
        wav_file (str): Path to wav file

    Returns:
        bool: If file is valid
    """
    return wav_file.endswith(".wav")


def make_sound(sound_path: Path = ROOT_DIR / "resources" / "pop.wav") -> None:
    """Play sound in sound_path.

    Args:
        sound_path (Path): Path to a wav sound file
    """
    sound_file = str(sound_path.absolute())
    if validate_sound_file(sound_file):
        wave_obj = sa.WaveObject.from_wave_file(sound_file)
        wave_obj.play()


def run_notify(command: str = CMD) -> None:
    """Run notification command.

    Args:
        command (str): Command to be run
    """
    subprocess.run(shlex.split(command))
    # TODO: implement configurable notification sound
    make_sound()
