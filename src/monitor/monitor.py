import time

class Monitor:
    def __init__(self, firewall):
        self.firewall = firewall

    def run(self):
        while True:
            time.sleep(1)

    def get_metrics(self):
        return {
            'current_connections': self.firewall.active_connections,
            'blocked_ips': len(self.firewall.blocked_ips),
            'denied_connections': self.firewall.denied_connections,
            'denied_by_threshold': self.firewall.denied_by_threshold,
            'denied_by_blocked': self.firewall.denied_by_blocked
        }
