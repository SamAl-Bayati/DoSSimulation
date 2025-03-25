import time

class Firewall:
    """
    A simple firewall-like mechanism that:
      - Tracks connection rate per IP
      - Blocks IPs that exceed a certain threshold
      - Automatically unblocks IPs after a block_time
      - Allows enabling/disabling mitigations
    """

    def __init__(self, rate_limit=30, block_threshold=50, block_time=60):
        """
        :param rate_limit: Connections allowed per minute (soft limit)
        :param block_threshold: If an IP exceeds this rate, it will be blocked
        :param block_time: Time in seconds to block an IP
        """
        self.rate_limit = rate_limit
        self.block_threshold = block_threshold
        self.block_time = block_time

        # Data structure to store: { ip: [timestamp1, timestamp2, ...], ...}
        self.connection_log = {}

        # Store blocked IP: { ip: unblock_timestamp }
        self.blocked_ips = {}

        # Mitigation flag
        self.mitigation_enabled = True

        # NEW: Counters for monitoring denied connections
        self.denied_connections = 0         # Total denied connections
        self.denied_by_threshold = 0        # Denied because connection rate exceeded block_threshold
        self.denied_by_blocked = 0          # Denied because IP was already blocked

    def enable_mitigation(self):
        """Enable mitigation strategies."""
        self.mitigation_enabled = True
        print("[FIREWALL] Mitigations enabled.")

    def disable_mitigation(self):
        """Disable mitigation strategies."""
        self.mitigation_enabled = False
        print("[FIREWALL] Mitigations disabled.")

    def is_blocked(self, ip):
        """Check if IP is currently blocked."""
        current_time = time.time()
        if ip in self.blocked_ips:
            if current_time >= self.blocked_ips[ip]:
                # Unblock IP
                del self.blocked_ips[ip]
                return False
            # Count the connection as denied because it is already blocked
            self.denied_connections += 1
            self.denied_by_blocked += 1
            return True
        return False

    def check_connection(self, ip):
        """
        Checks connection frequency from an IP.
        Updates logs and decides if the connection is allowed or blocked.
        Returns True if allowed, False if blocked.
        """
        if not self.mitigation_enabled:
            return True  # Allow all connections if mitigation is disabled

        current_time = time.time()

        if ip not in self.connection_log:
            self.connection_log[ip] = []
        self.connection_log[ip].append(current_time)

        # Clean old timestamps (older than 60s) for rate calculations
        one_minute_ago = current_time - 60
        self.connection_log[ip] = [ts for ts in self.connection_log[ip] if ts > one_minute_ago]

        # Check the rate
        current_rate = len(self.connection_log[ip])  # connections in the last minute

        if current_rate > self.block_threshold:
            # Block IP and count the denial
            self.blocked_ips[ip] = current_time + self.block_time
            self.denied_connections += 1
            self.denied_by_threshold += 1
            print(f"[FIREWALL] Blocking IP {ip} for {self.block_time} seconds (Rate={current_rate} > {self.block_threshold}).")
            return False

        if current_rate > self.rate_limit:
            print(f"[FIREWALL] Warning: IP {ip} is exceeding the soft rate limit (Rate={current_rate}).")

        return True
