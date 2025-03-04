import time

class Monitor:
    """
    Monitor class to collect metrics from the Firewall and Server.
    """

    def __init__(self, firewall):
        self.firewall = firewall
        self.current_connections = 0
        self.blocked_ips = 0

    def run(self):
        """
        Continuously update metrics.
        """
        while True:
            self.collect_metrics()
            time.sleep(1)

    def collect_metrics(self):
        """
        Collect metrics from the firewall.
        """
        self.blocked_ips = len(self.firewall.blocked_ips)
        # For current connections, sum all connections in the last minute
        self.current_connections = sum(len(timestamps) for timestamps in self.firewall.connection_log.values())

    def get_metrics(self):
        """
        Return the current metrics as a dictionary.
        """
        return {
            'current_connections': self.current_connections,
            'blocked_ips': self.blocked_ips
        }
