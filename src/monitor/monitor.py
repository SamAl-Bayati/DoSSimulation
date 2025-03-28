import time
import shared

class Monitor:
    def __init__(self, firewall):
        self.firewall = firewall

    def run(self):
        while True:
            self.firewall.prune_blocked_ips()
            time.sleep(1)

    def get_metrics(self):
        now = time.time()
        one_second_ago = now - 1
        self.firewall.udp_packet_timestamps = [
            ts for ts in self.firewall.udp_packet_timestamps
            if ts > one_second_ago
        ]
        udp_pps = len(self.firewall.udp_packet_timestamps)
        return {
            'current_connections': self.firewall.active_connections,
            'denied_connections': self.firewall.denied_connections,
            'server_crashed': shared.server_status['crashed'],
            'server_crashed_message': shared.server_status['message'],
            'udp_pps': udp_pps
        }
