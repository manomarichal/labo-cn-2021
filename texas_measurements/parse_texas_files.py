import csv
import os as os
import graphs
from datetime import datetime, timedelta
from Parser import Parser

VERBOSE = True

probes_file = open("./texas_measurements/probes.csv")
reader = csv.reader(probes_file)
probes = reader.__next__()
probes_file.close()

downtime_before = dict()
uptime_before = dict()

downtime_during = dict()
uptime_during = dict()

downtime_after = dict()
uptime_after = dict()

percent_more_downtime = dict()

PERIOD_DURATION = timedelta(days=10)
DATE_BEFORE_START = datetime(2021, 1, 31, 0, 0, 1)
DATE_START = datetime(2021, 2, 10, 0, 0, 0)
DATE_END = datetime(2021, 2, 19, 23, 59, 59)
DATE_AFTER_END = datetime(2021, 3, 1, 23, 59, 58)


# parse files
for probe in probes:
    data_file = "./texas_measurements/texas_data/" + probe + "_data.txt"
    if not os.path.isfile(data_file):
        continue

    if VERBOSE: print("========== probe " + probe + " ==========")
    parser_before = Parser(date_start=DATE_BEFORE_START, date_end=DATE_START)
    parser_during = Parser(date_start=DATE_START, date_end=DATE_END)
    parser_after = Parser(date_start=DATE_END, date_end=DATE_AFTER_END)

    parser_before.parse_file(data_file)
    parser_during.parse_file(data_file)
    parser_after.parse_file(data_file)

    uptime_before[probe] = parser_before.total_uptime
    downtime_before[probe] = parser_before.total_downtime
    uptime_during[probe] = parser_during.total_uptime
    downtime_during[probe] = parser_during.total_downtime
    uptime_after[probe] = parser_after.total_uptime
    downtime_after[probe] = parser_after.total_downtime

    if VERBOSE:
        print("before")
        print("\tuptime: ", parser_before.total_uptime)
        print("\tdowntime: ", parser_before.total_downtime)

        print("during")
        print("\tuptime: ", parser_during.total_uptime)
        print("\tdowntime: ", parser_during.total_downtime)

        print("after")
        print("\tuptime: ", parser_after.total_uptime)
        print("\tdowntime: ", parser_after.total_downtime)

x_axis = list()
y_axis_before = list()
y_axis_during = list()
y_axis_after = list()
y_axis_more_after = list()

for probe in probes:
    if not probe in downtime_before:
        continue
    x_axis.append(probe)
    y_axis_before.append(downtime_before[probe]/PERIOD_DURATION*100)
    y_axis_during.append(downtime_during[probe]/PERIOD_DURATION*100)
    y_axis_after.append(downtime_after[probe]/PERIOD_DURATION*100)
    y_axis_more_after.append((downtime_after[probe].seconds - downtime_before[probe].seconds)/(60*60))


graphs.make_bar_chart(x_axis, y_axis_before, "% of downtime before the snowstorm \n" + DATE_BEFORE_START.strftime("%m/%d/%Y") + "-" + DATE_START.strftime("%m/%d/%Y"), "./texas_measurements/graphs/downtime_before.png")
graphs.make_bar_chart(x_axis, y_axis_during, "% of downtime during the snowstorm \n" + DATE_START.strftime("%m/%d/%Y") + "-" + DATE_END.strftime("%m/%d/%Y"), "./texas_measurements/graphs/downtime_during.png")
graphs.make_bar_chart(x_axis, y_axis_after, "% of downtime after the snowstorm \n" + DATE_END.strftime("%m/%d/%Y") + "-" + DATE_AFTER_END.strftime("%m/%d/%Y"), "./texas_measurements/graphs/downtime_after.png")
graphs.make_bar_chart(x_axis, y_axis_more_after, "# hours more downtime after the snowstorm \n " + DATE_BEFORE_START.strftime("%m/%d/%Y") + "-" + DATE_START.strftime("%m/%d/%Y") + " vs " + DATE_END.strftime("%m/%d/%Y") + "-" + DATE_AFTER_END.strftime("%m/%d/%Y"), "./texas_measurements/graphs/after_vs_before.png", yticks=[-20, -15, -10, -5, 0, 5, 10, 15, 20, 25, 30])