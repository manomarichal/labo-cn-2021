from util import parse_line
from datetime import datetime, timedelta

class Parser:
    downtime = dict()
    total_uptime = timedelta()
    total_downtime = timedelta()

    def __init__(self, date_start=datetime(2021, 2, 10, 0, 0, 0), date_end=datetime(2021, 2, 19, 23, 59, 59)):
        self.date_start = date_start
        self.date_end = date_end
    
    def _update_uptime(self, date_start, duration):
        date_end = date_start + duration
        if date_end <= self.date_end:
            if date_start <= self.date_start:
                diff = date_end - self.date_start
                if diff > timedelta(seconds=0):
                    self.total_uptime += diff
            else:
                self.total_uptime += duration
        else:
            if date_start <= self.date_start:
                self.total_uptime += self.date_end - self.date_start
            else:
                diff = self.date_end - date_start
                if diff > timedelta(seconds=0):
                    self.total_uptime += diff

    def _update_downtime(self, date_start, duration):
        date_end = date_start + duration
        if date_end <= self.date_end:
            if date_start <= self.date_start:
                diff = date_end - self.date_start
                if diff > timedelta(seconds=0):
                    self.total_downtime += diff
            else:
                self.total_downtime += duration
        else:
            if date_start <= self.date_start:
                self.total_downtime += self.date_end - self.date_start
            else:
                diff = self.date_end - date_start
                if diff > timedelta(seconds=0):
                    self.total_downtime += diff

    def parse_file(self, filename):
        f = open(filename)
        for line in f:
            date_connected_start, date_disconnected_start, duration_connected, duration_disconnected = parse_line(line)

            self._update_uptime(date_connected_start, duration_connected)
            self._update_downtime(date_disconnected_start, duration_disconnected)



