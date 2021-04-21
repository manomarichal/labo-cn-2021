import json
from custom_measurements.statistic import Statistic, EmptyStatistic
from custom_measurements.data_handler import DataHandler, rating_color
from custom_measurements.probe_lists import foreign_probes, local_probes

current_dir = "./measurements/"
output_dir = "./ratings/"
files = [
    "chaos",
    "gaia",
    "primal",
    "aether"
]
optimum_output = "optimum.txt"


def get_best_server_per_probe(data_dict, probe_id):
    """
    looks at all data and determines the best possible server for a specific probe
    (based on average delay)
    :param data_dict:
    :param probe_id
    :return:
    """
    min_delay = None
    best_server = None
    for key in data_dict.keys():
        current_handler = data_dict[key]
        current_del = current_handler.get_avg_delay_from_probe(probe_id)
        if min_delay is None:
            min_delay = current_del
            best_server = key
        if min_delay > current_del:
            min_delay = current_del
            best_server = key
    return best_server, min_delay


def handler_output():
    all_data = dict()
    for file in files:
        ping_results = dict()
        filename = current_dir + file + ".json"
        f = open(filename,)
        js = json.load(f)
        for item in js:
            rtt_list = item["result"]
            rtt = []
            for rtt_item in rtt_list:
                if "rtt" in rtt_item.keys():
                    rtt.append(rtt_item["rtt"])
            prb_id = int(item["prb_id"])
            sent = int(item["sent"])
            received = int(item["rcvd"])
            if len(rtt) != 0:
                new_stat = Statistic(prb_id, rtt, sent, received)
            else:
                new_stat = EmptyStatistic(prb_id, sent)
            if prb_id not in ping_results.keys():
                ping_results[prb_id] = [new_stat]
            else:
                ping_results[prb_id].append(new_stat)

        dh = DataHandler(ping_results, file)
        all_data[file] = dh

    for server_name in files:
        curr_local_probes = local_probes[server_name]
        ratings = all_data[server_name].generate_ratings_average_delay(foreign_probes)
        filename = output_dir + str(server_name) + ".txt"
        of = open(filename, "w")
        of.write("====== foreign probe ratings: ======\n")
        for k in ratings.keys():
            of.write(str(k) + " : " + str(ratings[k]) + ", " + str(rating_color(ratings[k])))
            of.write("\n")

        ratings = all_data[server_name].generate_ratings_average_delay(curr_local_probes)
        of.write("\n====== local probe ratings: ======\n")
        for k in ratings.keys():
            of.write(str(k) + " : " + str(ratings[k]) + ", " + str(rating_color(ratings[k])))
            of.write("\n")
        of.close()

    optimal = open(output_dir + optimum_output, "w")
    for probe_id in foreign_probes:
        p = get_best_server_per_probe(all_data, probe_id)
        line = str(probe_id) + ": " + p[0]
        line += ", delay is " + str(p[1])
        optimal.write(line + "\n")

    optimal.close()
    return all_data
