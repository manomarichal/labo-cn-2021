from custom_measurements.measurements_handler import *
from custom_measurements.probe_lists import foreign_probes, local_probes
from matplotlib import pyplot as plt
import numpy as np
"""
will write all necessary data to dicts/json-files
"""
stat_dir = "./statistics/"


def output_statistics(server_name, data_handler):
    filename = stat_dir + server_name + ".txt"
    f = open(filename, "w")
    loc_probes = local_probes[server_name]
    # first the average round-trip time per probe pinging to this server
    avg_delay = data_handler.get_avg_delay()
    avg_loc_delay = data_handler.get_avg_delay(loc_probes)
    avg_for_delay = data_handler.get_avg_delay(foreign_probes)
    avg_rel = data_handler.get_reliability()
    avg_for_rel = data_handler.get_reliability(foreign_probes)
    avg_loc_rel = data_handler.get_reliability(loc_probes)
    f.write("global average delay " + str(avg_delay) + "\n")
    f.write("local average delay " + str(avg_loc_delay) + "\n")
    f.write("foreign average delay " + str(avg_for_delay) + "\n")
    f.write("global reliability " + str(avg_rel) + "%\n")
    f.write("local reliability " + str(avg_loc_rel) + "%\n")
    f.write("foreign reliability " + str(avg_for_rel) + "%\n")

    pass


def make_reliability_dict(all_data):
    result = dict()
    for server_name in all_data.keys():
        loc_probes = local_probes[server_name]
        item = dict()
        data_handler = all_data[server_name]
        item["average_reliability"] = data_handler.get_reliability()
        item["average_foreign_reliability"] = data_handler.get_reliability(foreign_probes)
        item["average_local_reliability"] = data_handler.get_reliability(loc_probes)
        result[server_name] = item

    return result


def make_avg_delay_dict(all_data):
    result = dict()
    for server_name in all_data.keys():
        loc_probes = local_probes[server_name]
        item = dict()
        data_handler = all_data[server_name]
        item["average_delay"] = data_handler.get_avg_delay()
        item["average_foreign_delay"] = data_handler.get_avg_delay(foreign_probes)
        item["average_local_delay"] = data_handler.get_avg_delay(loc_probes)
        result[server_name] = item

    return result


def make_min_delay_dict(all_data):
    result = dict()
    for server_name in all_data.keys():
        loc_probes = local_probes[server_name]
        item = dict()
        data_handler = all_data[server_name]
        item["minimal_delay"] = data_handler.get_min_delay()
        item["minimal_foreign_delay"] = data_handler.get_min_delay(foreign_probes)
        item["minimal_local_delay"] = data_handler.get_min_delay(loc_probes)
        result[server_name] = item

    return result


def make_max_delay_dict(all_data):
    result = dict()
    for server_name in all_data.keys():
        loc_probes = local_probes[server_name]
        item = dict()
        data_handler = all_data[server_name]
        item["maximal_delay"] = data_handler.get_max_delay()
        item["maximal_foreign_delay"] = data_handler.get_max_delay(foreign_probes)
        item["maximal_local_delay"] = data_handler.get_max_delay(loc_probes)
        result[server_name] = item

    return result


def make_all_delays_dict(all_data):
    result = dict()
    for server_name in all_data.keys():
        data_handler = all_data[server_name]
        delay_list = data_handler.get_all_average_delays(foreign_probes)
        result[server_name] = delay_list
    return result


def make_bar_chart(x_axis, y_axis, title, special_range=None):
    filename = stat_dir + title + ".png"
    f = open(filename, "w")
    font = {'fontname':'Arial'}
    f.close()
    height = y_axis
    bars = x_axis
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height, color=(1.00, 0.40, 0.50, 0.8), width=-0.40)
    plt.xticks(y_pos, x_axis, rotation=90)
    plt.title('title',**font)
    if special_range is not None:
        plt.ylim(special_range)
    plt.title(title)
    # plt.show()
    plt.savefig(filename)


def make_graphs(ad):
    rd = make_reliability_dict(ad)
    add = make_avg_delay_dict(ad)
    mindd = make_min_delay_dict(ad)
    maxdd = make_max_delay_dict(ad)
    all_delays_dict = make_all_delays_dict(ad)
    avg_delay_array = []
    reliability_array = []
    min_delay_array = []
    max_delay_array = []
    server_array = []
    for server in add.keys():
        server_array.append(server)
        avg_delay_array.append(add[server]["average_delay"])
        min_delay_array.append(mindd[server]["minimal_delay"])
        max_delay_array.append(maxdd[server]["maximal_delay"])
        reliability_array.append(rd[server]["average_reliability"])
    # make_bar_chart(server_array, avg_delay_array, "average delay")
    # make_bar_chart(server_array, min_delay_array, "minimal delay")
    # make_bar_chart(server_array, max_delay_array, "maximal delay")
    # make_bar_chart(server_array, reliability_array, "average reliability", special_range=(90, 100))
    # for server_name in all_delays_dict.keys():
    #     all_delays_array = all_delays_dict[server_name]
    #     all_probes = foreign_probes
    #     title = "all delays for " + str(server_name)
    #     make_bar_chart(all_probes, all_delays_array, title)



ad = handler_output()
for server in files:
    output_statistics(server, ad[server])
make_graphs(ad)
