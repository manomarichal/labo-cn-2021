import csv
from parser import Parser

probes_file = open("./probes.csv")
reader = csv.reader(probes_file)
probes = reader.__next__()
probes_file.close()

downtime = dict()
uptime = dict()

# parse files
for probe in probes:
    print("========== probe " + probe + " ==========")
    parser = Parser()
    parser.parse_file("./texas_data/" + probe + "_data.txt")
    uptime[probe] = parser.total_uptime
    downtime[probe] = parser.total_downtime

    print(parser.total_downtime)
    print(parser.total_uptime)



