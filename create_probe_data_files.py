import csv

probes_file = open("../probes.csv")
reader = csv.reader(probes_file)
probes = reader.__next__()


# create files
for probe in probes:
    f = open("../texas_downtime_probes/" + probe + "_data.txt", 'x')
    f.write(probe)
    f.close()