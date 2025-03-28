import time
import shared

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
        Return current metrics + server crash info.
        """
        return {
            'current_connections': self.firewall.active_connections,
            'denied_connections': self.firewall.denied_connections,
            'server_crashed': shared.server_status['crashed'],
            'server_crashed_message': shared.server_status['message']
        }
