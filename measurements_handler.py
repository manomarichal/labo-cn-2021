import json
from statistic import Statistic, EmptyStatistic
from data_handler import DataHandler
from probe_lists import foreign_probes, local_probes

current_dir = "./measurements/"
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
        dst = None
        for item in js:
            if dst is None:
                dst = item["dst_name"]
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

        DH = DataHandler(ping_results, dst)
        all_data[file] = DH

    for fp in foreign_probes:
        print(all_data["gaia"].get_delay_spread_from_probe(fp))
    pass
