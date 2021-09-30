from datetime import date, timedelta
from typing import Any, Dict, List


class SimpleGCalendarPrinter:

    def __init__(
        self,
        events: List[Dict[str, Any]],
        general_params: Dict[str, Any],
        calendar_params: Dict[str, Any],
    ) -> None:
        self.events = events

    def CalQuery(self, cmd, count=1):
        # convert now to midnight this morning and use for default
        start = self.now.replace(hour=0,
                                 minute=0,
                                 second=0,
                                 microsecond=0)

        # convert start date to the beginning of the week or month
        if cmd == 'calw':
            start = (start - timedelta(days=start.weekday()))
            end = (start + timedelta(days=(count * 7)))
        else:  # cmd == 'calm':
            start = (start.replace(day=1))
            end_month = (start.month + 1)
            end_year = start.year
            if end_month == 13:
                end_month = 1
                end_year += 1
            end = start.replace(month=end_month, year=end_year)
            days_in_month = (end - start).days
            offset_days = int(start.strftime('%w'))
            if self.options['cal_monday']:
                offset_days -= 1
                if offset_days < 0:
                    offset_days = 6
            total_days = (days_in_month + offset_days)
            count = total_days // 7
            if total_days % 7:
                count += 1

        self._GraphEvents(cmd, start, count, self.events)

    def _GraphEvents(self, cmd, start_datetime, count, event_list):
        # ignore started events (i.e. events that start previous day and end
        # start day)

        color_border = self.options['color_border']

        while (len(event_list) and event_list[0]['s'] < start_datetime):
            event_list = event_list[1:]

        day_width_line = self.options['cal_width'] * self.printer.art['hrz']
        days = 7 if self.options['cal_weekend'] else 5
        # Get the localized day names... January 1, 2001 was a Monday
        day_names = [date(2001, 1, i + 1).strftime('%A') for i in range(days)]
        if not self.options['cal_monday'] or not self.options['cal_weekend']:
            day_names = day_names[6:] + day_names[:6]

        def build_divider(left, center, right):
            return (
                self.printer.art[left] + day_width_line +
                ((days - 1) * (self.printer.art[center] + day_width_line)) +
                self.printer.art[right]
            )

        week_top = build_divider('ulc', 'ute', 'urc')
        week_divider = build_divider('lte', 'crs', 'rte')
        week_bottom = build_divider('llc', 'bte', 'lrc')
        empty_day = self.options['cal_width'] * ' '

        if cmd == 'calm':
            # month titlebar
            month_title_top = build_divider('ulc', 'hrz', 'urc')
            self.printer.msg(month_title_top + '\n', color_border)

            month_title = start_datetime.strftime('%B %Y')
            month_width = (self.options['cal_width'] * days) + (days - 1)
            month_title += ' ' * (month_width - self._printed_len(month_title))

            self.printer.art_msg('vrt', color_border)
            self.printer.msg(month_title, self.options['color_date'])
            self.printer.art_msg('vrt', color_border)

            month_title_bottom = build_divider('lte', 'ute', 'rte')
            self.printer.msg('\n' + month_title_bottom + '\n', color_border)
        else:
            # week titlebar
            # month title bottom takes care of this when cmd='calm'
            self.printer.msg(week_top + '\n', color_border)

        # weekday labels
        self.printer.art_msg('vrt', color_border)
        for day_name in day_names:
            day_name += ' ' * (
                    self.options['cal_width'] - self._printed_len(day_name)
            )
            self.printer.msg(day_name, self.options['color_date'])
            self.printer.art_msg('vrt', color_border)

        self.printer.msg('\n' + week_divider + '\n', color_border)
        cur_month = start_datetime.strftime('%b')

        # get date range objects for the first week
        if cmd == 'calm':
            day_num = self._cal_monday(int(start_datetime.strftime('%w')))
            start_datetime = (start_datetime - timedelta(days=day_num))
        start_week_datetime = start_datetime
        end_week_datetime = (start_week_datetime + timedelta(days=7))

        for i in range(count):
            # create and print the date line for a week
            for j in range(days):
                if cmd == 'calw':
                    d = (start_week_datetime +
                         timedelta(days=j)).strftime('%d %b')
                else:  # (cmd == 'calm'):
                    d = (start_week_datetime +
                         timedelta(days=j)).strftime('%d')
                    if cur_month != (start_week_datetime +
                                     timedelta(days=j)).strftime('%b'):
                        d = ''
                tmp_date_color = self.options['color_date']

                fmt_now = (start_week_datetime +
                           timedelta(days=j)).strftime('%d%b%Y')
                if self.now.strftime('%d%b%Y') == fmt_now:
                    tmp_date_color = self.options['color_now_marker']
                    d += ' **'

                d += ' ' * (self.options['cal_width'] - self._printed_len(d))

                # print dates
                self.printer.art_msg('vrt', color_border)
                self.printer.msg(d, tmp_date_color)

            self.printer.art_msg('vrt', color_border)
            self.printer.msg('\n')

            week_events = self._get_week_events(
                    start_week_datetime, end_week_datetime, event_list
            )

            # get date range objects for the next week
            start_week_datetime = end_week_datetime
            end_week_datetime = (end_week_datetime + timedelta(days=7))

            while True:
                # keep looping over events by day, printing one line at a time
                # stop when everything has been printed
                done = True
                self.printer.art_msg('vrt', color_border)
                for j in range(days):
                    if not week_events[j]:
                        # no events today
                        self.printer.msg(
                                empty_day + self.printer.art['vrt'],
                                color_border
                        )
                        continue

                    curr_event = week_events[j][0]
                    print_len, cut_idx = self._get_cut_index(curr_event.title)
                    padding = ' ' * (self.options['cal_width'] - print_len)

                    self.printer.msg(
                            curr_event.title[:cut_idx] + padding,
                            curr_event.color
                    )

                    # trim what we've already printed
                    trimmed_title = curr_event.title[cut_idx:].strip()

                    if trimmed_title == '':
                        week_events[j].pop(0)
                    else:
                        week_events[j][0] = \
                                curr_event._replace(title=trimmed_title)

                    done = False
                    self.printer.art_msg('vrt', color_border)

                self.printer.msg('\n')
                if done:
                    break

            if i < range(count)[len(range(count)) - 1]:
                self.printer.msg(week_divider + '\n', color_border)
            else:
                self.printer.msg(week_bottom + '\n', color_border)
