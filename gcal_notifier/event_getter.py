from .utils import CONFIG

from gcsa.google_calendar import GoogleCalendar

def make_conn(calendar: str = 'primary',
              creds_file: str = CONFIG+'/credentials.json'
              ) -> GoogleCalendar:
    return GoogleCalendar(calendar=calendar,
                        credentials_path=creds_file)
