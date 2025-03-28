import time

class Firewall:
    def __init__(self, rate_limit=30, block_threshold=50, block_time=60):
        self.rate_limit = rate_limit
        self.block_threshold = block_threshold
        self.block_time = block_time
        self.connection_log = {}
        self.blocked_ips = {}
        self.mitigation_enabled = True
        self.active_connections = 0
        self.denied_connections = 0
        self.udp_packet_timestamps = []

    def enable_mitigation(self):
        self.mitigation_enabled = True
        print("[FIREWALL] Mitigations enabled.")

    def disable_mitigation(self):
        self.mitigation_enabled = False
        print("[FIREWALL] Mitigations disabled.")

    def reset_caches(self):
        self.connection_log = {}
        self.blocked_ips = {}
        self.active_connections = 0
        self.denied_connections = 0
        self.udp_packet_timestamps = []
        print("[FIREWALL] All caches/logs have been reset.")

    def is_blocked(self, ip):
        current_time = time.time()
        if ip in self.blocked_ips:
            if current_time >= self.blocked_ips[ip]:
                del self.blocked_ips[ip]
                return False
            self.denied_connections += 1
            return True
        return False

    def check_connection(self, ip):
        if not self.mitigation_enabled:
            self.active_connections += 1
            return True

        current_time = time.time()
        if ip not in self.connection_log:
            self.connection_log[ip] = []
        self.connection_log[ip].append(current_time)
        one_minute_ago = current_time - 60
        self.connection_log[ip] = [ts for ts in self.connection_log[ip] if ts > one_minute_ago]
        current_rate = len(self.connection_log[ip])

        if current_rate > self.block_threshold:
            self.blocked_ips[ip] = current_time + self.block_time
            self.denied_connections += 1
            print(f"[FIREWALL] Blocking IP {ip} for {self.block_time}s (Rate={current_rate} > {self.block_threshold}).")
            return False

        if current_rate > self.rate_limit:
            print(f"[FIREWALL] Warning: IP {ip} is exceeding the soft rate limit (Rate={current_rate}).")

        self.active_connections += 1
        return True

    def end_connection(self, ip):
        if self.active_connections > 0:
            self.active_connections -= 1

    def record_udp_packet(self):
        self.udp_packet_timestamps.append(time.time())

    def prune_blocked_ips(self):
        current_time = time.time()
        for ip, unblock_time in list(self.blocked_ips.items()):
            if current_time >= unblock_time:
                del self.blocked_ips[ip]
