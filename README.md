# SimpleGCalendarNotifier

### A simple and lightweight GoogleCalendar notifier for Linux

This app is focused on giving versatility and simplicity, and present a
very lightweight command-line application that reminds you of your events
in Google Calendar.

The project was inspired by [gcalcli](https://github.com/insanum/gcalcli),
and looking for more bare-bones features and that could handle multiple
Google accounts and calendars.

Installation
------------

For now, this package is only available through [PyPi](https://pypi.org/)

### Install from PyPi
```sh
pip install gcal_notifier
```

Features
--------

- Fetch Google events from all accounts
- Notify events
- Uses Cron jobs to keep everything as minimal as possible

Usage
-----

```sh
gcal_notifier [get|remind]
usage: gcal_notifier [-h] [get|remind]

A simple and lightweight GoogleCalendar notifier for Linux

positional arguments:
  [get|remind]  Use "get" to get events and "remind" to run reminders

optional arguments:
  -h, --help      show this help message and exit
```

### Credentials

For all of this to work, you have to create your credentials for each account
you want to use.
Note: this section was copied and pasted from the [gcsa](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html) README.

1. Create a new [Google Cloud Platform (GCP) project](https://developers.google.com/workspace/guides/create-project)

2. Configure the [OAuth consent screen](https://developers.google.com/workspace/guides/create-credentials#configure_the_oauth_consent_screen)

3. [Create a OAuth client ID credential](https://developers.google.com/workspace/guides/create-credentials#create_a_oauth_client_id_credential)
and download the `credentials.json` file

4. Put downloaded `credentials.json` file into `~/.config/gcal_notifier/default`

See more options in [Authentication](https://google-calendar-simple-api.readthedocs.io/en/latest/authentication.html#authentication).

Note:

On the first run, your application will prompt you to the default browser to get permissions from you to use your calendar.
This will create token.pickle file in the same folder.

Setting Up
----------

After having your `credentials.json` file(s), you can run `gcal_notifier get`
to see if everything works properly.

If it does, it's time to set up your cron jobs.

1. Run `crontab -e` to edit your cron jobs.

2. Choose the intervals that you want to run `get` and `remind`. This means
that you can fetch events in a different interval that you check for reminders.
My personal preference, for example, is:
```sh
*/10 * * * *  gcal_notifier get
* * * * *  gcal_notifier remind
```
So it runs every 10 minutes to fetch events, but looks for reminders every minute.

That's it! You're all set up!

Configuration
-------------

You can configure some things for now (and hopefully more later), and all the
configurations are done in a file that sits in `~/.config/gcal_notifier/config.ini`

A sample of every configuration supported is:
```ini
[GENERAL]
# Returns only one event for recurrent events. Default is true
single_events = true
# How to order the events. Default (and recommended) is startTime
order_by = startTime

[CALENDAR1]
# Name given to the calendar. Default is 'Calendar'
name = NAME1
# Name or ID of the calendar. Required.
calendar = example@gmail.com
# Reminders to your events, up to 5 integers separated by commas. Default is None
default_reminders = 10,0
# Path to the credentials file. Default is ~/.config/gcal_notifier/credentials.json
# credentials = ~/.config/gcal_notifier/credentials_file.json

[CALENDAR2]
name = NAME2
calendar = xxxxxxxxxxxxxxxxxxxxxxxx@group.calendar.google.com
default_reminders = 10,0
credentials = ~/.config/gcal_notifier/credentials_other_account.json

[CALENDAR3]
name = NAME3
calendar = other@gmail.com
.
.
.
```

## Help wanted!

If you find this project useful, please feel free to contribute or report an issue.
You can always email me as thalesaknunes22@gmail.com

### Happy Coding!
