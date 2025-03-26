import time

class Firewall:
    def __init__(self, rate_limit=30, block_threshold=50, block_time=60):
        self.rate_limit = rate_limit
        self.block_threshold = block_threshold
        self.block_time = block_time

        self.connection_log = {}
        self.blocked_ips = {}
        self.mitigation_enabled = True

        # Tracks how many connections are currently active (not blocked)
        self.active_connections = 0
        
        # A single cumulative count of how many connections have been denied
        self.denied_connections = 0

    def enable_mitigation(self):
        self.mitigation_enabled = True
        print("[FIREWALL] Mitigations enabled.")

    def disable_mitigation(self):
        self.mitigation_enabled = False
        print("[FIREWALL] Mitigations disabled.")

    def is_blocked(self, ip):
        """
        If IP is in blocked_ips and its block time hasn't expired, we block it.
        If block time expired, we remove from blocked_ips.
        """
        current_time = time.time()
        if ip in self.blocked_ips:
            unblock_time = self.blocked_ips[ip]
            if current_time >= unblock_time:
                # block time is over; remove from blocked list
                del self.blocked_ips[ip]
                return False
            # still blocked
            self.denied_connections += 1
            return True
        return False

    def check_connection(self, ip):
        """Return True if connection is allowed, False if blocked."""
        if not self.mitigation_enabled:
            # No mitigations at all
            self.active_connections += 1
            return True

        current_time = time.time()

        # Track the timestamps for this IP
        if ip not in self.connection_log:
            self.connection_log[ip] = []
        self.connection_log[ip].append(current_time)

        # Keep only timestamps from the last 60 seconds
        one_minute_ago = current_time - 60
        self.connection_log[ip] = [ts for ts in self.connection_log[ip] if ts > one_minute_ago]
        current_rate = len(self.connection_log[ip])

        # Check if rate is above block threshold
        if current_rate > self.block_threshold:
            # Block IP for self.block_time
            self.blocked_ips[ip] = current_time + self.block_time
            self.denied_connections += 1
            print(f"[FIREWALL] Blocking IP {ip} for {self.block_time} seconds (Rate={current_rate} > {self.block_threshold}).")
            return False

        # If above soft rate limit, just warn
        if current_rate > self.rate_limit:
            print(f"[FIREWALL] Warning: IP {ip} is exceeding the soft rate limit (Rate={current_rate}).")

        # Otherwise, connection is allowed
        self.active_connections += 1
        return True

    def end_connection(self, ip):
        """Called when the connection closes."""
        if self.active_connections > 0:
            self.active_connections -= 1

    def prune_blocked_ips(self):
        """Periodically remove IPs whose block time has expired."""
        current_time = time.time()
        for ip, unblock_time in list(self.blocked_ips.items()):
            if current_time >= unblock_time:
                del self.blocked_ips[ip]
