import json
from statistic import Statistic, EmptyStatistic
from data_handler import DataHandler, rating_color
from probe_lists import foreign_probes, local_probes

current_dir = "./measurements/"
output_dir = "./ratings/"
files = [
    "chaos",
    "gaia",
    "primal",
    "aether"
]

if __name__ == "__main__":
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
            id = int(item["prb_id"])
            sent = int(item["sent"])
            received = int(item["rcvd"])
            if len(rtt) != 0:
                new_stat = Statistic(id, rtt, sent, received)
            else:
                new_stat = EmptyStatistic(id, sent)
            if id not in ping_results.keys():
                ping_results[id] = [new_stat]
            else:
                ping_results[id].append(new_stat)

        DH = DataHandler(ping_results, file)
        all_data[file] = DH

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

    pass
