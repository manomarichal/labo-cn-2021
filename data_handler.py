from statistic import Statistic, EmptyStatistic


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
                if (stat.max_rtt < min_delay) or (min_delay is None):
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
