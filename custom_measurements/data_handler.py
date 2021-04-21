from statistic import Statistic, EmptyStatistic

min_color = [255, 0, 0]
max_color = [0, 255, 0]

def rating_color(rating):
    diff = 1 - rating
    res = [
        int(rating*min_color[0]),
        int(diff*max_color[1]),
        0
    ]
    return res


class DataHandler:
    def __init__(self, stats, dst):
        """
        :param stats: a dictionary with all parsed data
        :param dst: the destination to which the measurements have been made
        """
        self.stats = stats
        self.dst = dst

    def get_max_delay_from_probe(self, probe_id):
        """
        gets the max delay for a probe across all its measurements
        :param probe_id: the id of the requested probe
        :return:
        """
        statistics = self.stats[probe_id]
        max_delay = -1
        for stat in statistics:
            if type(stat) != EmptyStatistic:
                if stat.max_rtt > max_delay:
                    max_delay = stat.max_rtt
        return max_delay

    def get_min_delay_from_probe(self, probe_id):
        """
        gets the minimal delay for a probe across all its measurements
        :param probe_id: the id of the requested probe
        :return:
        """
        statistics = self.stats[probe_id]
        min_delay = None
        for stat in statistics:
            if type(stat) != EmptyStatistic:
                if min_delay is None:
                    min_delay = stat.max_rtt
                if stat.max_rtt < min_delay:
                    min_delay = stat.max_rtt
        return min_delay

    def get_avg_delay_from_probe(self, probe_id):
        """
        gets the average delay for a probe across all its measurements
        :param probe_id: the id of the requested probe
        :return:
        """
        statistics = self.stats[probe_id]
        total_measurements = 0
        total_delay = 0
        for stat in statistics:
            total_delay += sum(stat.rtt)
            total_measurements += len(stat.rtt)
        return total_delay/total_measurements

    def get_reliability_from_probe(self, probe_id):
        """
        calculates how many packets sent by a probe are also returned
        :param probe_id: the id of the requested probe
        :return:
        """
        statistics = self.stats[probe_id]
        total_packets_sent = 0
        total_packets_received = 0
        for stat in statistics:
            total_packets_sent += stat.sent
            total_packets_received += stat.received
        return total_packets_received/total_packets_sent

    def get_delay_spread_from_probe(self, probe_id):
        """
        :param probe_id: the requested probe
        :return: the difference between max_rtt and min_rtt
        """
        mx = self.get_max_delay_from_probe(probe_id)
        mn = self.get_min_delay_from_probe(probe_id)
        return mx-mn

    def get_max_delay(self):
        """
        :return: the max delay across all probes
        """
        max_delay = None
        for probe_id in self.stats.keys():
            probe_delay = self.get_max_delay_from_probe(probe_id)
            if max_delay is None:
                max_delay = probe_delay
            if max_delay < probe_delay:
                max_delay = probe_delay
        return max_delay

    def get_min_delay(self):
        """
        :return: the min delay across all probes
        """
        min_delay = None
        for probe_id in self.stats.keys():
            probe_delay = self.get_min_delay_from_probe(probe_id)
            if min_delay is None:
                min_delay = probe_delay
            if min_delay > probe_delay:
                min_delay = probe_delay
        return min_delay

    def get_highest_avg_delay(self, probes):
        max_delay = None
        for probe_id in probes:
            delay = self.get_avg_delay_from_probe(probe_id)
            if max_delay is None:
                max_delay = delay
            if max_delay < delay:
                max_delay = delay
        return max_delay

    def get_lowest_avg_delay(self, probes):
        min_delay = None
        for probe_id in probes:
            delay = self.get_avg_delay_from_probe(probe_id)
            if min_delay is None:
                min_delay = delay
            if min_delay > delay:
                min_delay = delay
        return min_delay

    def generate_ratings_average_delay(self, probes):
        """
        generates a dict of ratings per probe_id in probes, based on the average delay in this probe
        :param probes:
        :return:
        """
        result = dict()
        max_delay = self.get_highest_avg_delay(probes)  # offset
        min_delay = self.get_lowest_avg_delay(probes)
        delay_range = max_delay - min_delay
        delay_factor = delay_range
        for probe_id in probes:
            avg_delay = self.get_avg_delay_from_probe(probe_id)
            print("delay_range: ", delay_range)
            print("delay_factor: ", delay_factor)
            print("average_delay:", avg_delay)
            delay_rating = (avg_delay - min_delay) / delay_factor
            result[probe_id] = 1-delay_rating
            # higher delay should get a lower rating
        return result
