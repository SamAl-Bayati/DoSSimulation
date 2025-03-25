import time

class Monitor:
    def __init__(self, firewall):
        self.firewall = firewall
        self.current_connections = 0
        self.blocked_ips = 0

    def run(self):
        while True:
            self.collect_metrics()
            time.sleep(1)

    def collect_metrics(self):
        self.blocked_ips = len(self.firewall.blocked_ips)
        self.current_connections = sum(len(timestamps) for timestamps in self.firewall.connection_log.values())

    def get_metrics(self):
        return {
            'current_connections': self.current_connections,
            'blocked_ips': self.blocked_ips,
            'denied_connections': self.firewall.denied_connections,
            'denied_by_threshold': self.firewall.denied_by_threshold,
            'denied_by_blocked': self.firewall.denied_by_blocked
        }
