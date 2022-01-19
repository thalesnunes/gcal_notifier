import shlex
import subprocess
from pathlib import Path
from typing import NoReturn

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
) -> NoReturn:
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
) -> NoReturn:
    """Run notification command.

    Args:
        command (str): Command to be run
        sound_path (Path): Path to a wav sound file
    """
    subprocess.run(shlex.split(command))
    make_sound(sound_path)
