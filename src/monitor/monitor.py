import time

class Monitor:
    def __init__(self, firewall):
        self.firewall = firewall

    def run(self):
        while True:
            # Periodically prune any IPs whose block time has expired
            self.firewall.prune_blocked_ips()
            time.sleep(1)

    def get_metrics(self):
        """
        Return current metrics:
         - current_connections: how many are currently active
         - denied_connections: how many have been denied total (cumulative)
        """
        return {
            'current_connections': self.firewall.active_connections,
            'denied_connections': self.firewall.denied_connections
        }
