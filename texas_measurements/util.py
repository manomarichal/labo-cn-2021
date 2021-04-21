from datetime import datetime, timedelta

def get_duration(string):
    number = ""
    total_time = 0
    for c in string:
        if c == "d":
            total_time += int(number)*24*60
            number = ""
        elif c == "h":
            total_time += int(number)*60
            number = ""
        elif c == "m":
            total_time += int(number)
            number = ""
        else:
            number += c

    return timedelta(0, total_time*60, 0)

def parse_line(line):
    section = 0
    date_con = ""
    time_con = ""
    duration_con = ""

    date_discon = ""
    time_discon = ""
    duration_discon = ""

    for c in line:
        if c == " " or c == "\t":
            if c == " " and section not in {1, 2, 4, 5}:
                section += 1
            elif c == "\t":
                section += 1
        elif section == 0:
            date_con += c
        elif section == 1:
            time_con += c
        elif section == 2:
            duration_con += c
        elif section == 3:
            date_discon += c
        elif section == 4:
            time_discon += c
        elif section == 5:
            duration_discon += c

    datetime_con = datetime(year=int(date_con[:4]), month=int(date_con[5:-3]), day=int(date_con[-2:]),
                            hour=int(time_con[:2]), minute=int(time_con[3:5]), second=int(time_con[-2:]))

    datetime_discon = datetime(year=int(date_discon[:4]), month=int(date_discon[5:-3]), day=int(date_discon[-2:]),
                            hour=int(time_discon[:2]), minute=int(time_discon[3:5]), second=int(time_discon[-2:]))

    total_time_con = get_duration(duration_con)
    total_time_discon = get_duration(duration_discon)
    return datetime_con, datetime_discon, total_time_con, total_time_discon