

class Statistic:
    def __init__(self, probe_id, rtt, sent, received):
        """
        :param probe_id: the probe id
        :param rtt: a list of rtt-values for all sent pings
        :param sent: the amount of pings sent
        :param received: the amount of responses received
        """
        self.id = probe_id
        self.rtt = rtt
        self.sent = sent
        self.received = received
        self.avg_rtt = sum(rtt)/len(rtt)    # average response time
        self.max_rtt = max(rtt)             # max response time
        self.min_rtt = min(rtt)             # min response time


class EmptyStatistic:
    def __init__(self, probe_id, sent):
        """
        for probes that didn't get a proper response listed in the json
        :param probe_id: the probe id
        :param sent: the amount of pings sent
        """
        self.id = probe_id
        self.rtt = []
        self.sent = sent
        self.received = 0
