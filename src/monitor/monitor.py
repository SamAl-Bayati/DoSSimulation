import time

class Monitor:
    def __init__(self, firewall):
        self.firewall = firewall

    def run(self):
        while True:
            # Periodically prune old logs and blocks
            self.firewall.prune_connection_logs()
            self.firewall.prune_expired_blocks()
            time.sleep(1)

    def get_metrics(self):
        """
        Return rolling metrics from the last 60 seconds:
          - current_connections: number of active live sockets
          - blocked_ips: number of IPs currently in self.blocked_ips
          - denied_by_threshold: # denies in last 60s from threshold
          - denied_by_blocked: # denies in last 60s from IPs that were already blocked
        """
        now = time.time()
        one_minute_ago = now - 60

        # Prune old denies
        self.firewall.denied_threshold_log = [
            ts for ts in self.firewall.denied_threshold_log if ts > one_minute_ago
        ]
        self.firewall.denied_block_log = [
            ts for ts in self.firewall.denied_block_log if ts > one_minute_ago
        ]

        # Also prune block list if any have expired
        self.firewall.prune_expired_blocks()

        return {
            'current_connections': self.firewall.active_connections,
            'blocked_ips': len(self.firewall.blocked_ips),
            'denied_by_threshold': len(self.firewall.denied_threshold_log),
            'denied_by_blocked': len(self.firewall.denied_block_log),
        }
