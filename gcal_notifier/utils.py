import os
from datetime import datetime, timedelta
import simpleaudio as sa

CONFIG = os.path.expanduser('~/.config/gcal_notifier')
GENERAL_PARAMS = {'time_min': datetime.now(),
                  'time_max': datetime.now()+timedelta(days=1),
                  'order_by': 'startTime',
                  'single_events': True}

def validate_sound_file(path: str):
    assert path.endswith('.wav')

def make_sound(sound_file: str = ''):
    validate_sound_file(sound_file)
    wave_obj = sa.WaveObject.from_wave_file(sound_file)
    wave_obj.play()
