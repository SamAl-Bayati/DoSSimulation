import time

class Firewall:
    """
    A simple firewall-like mechanism that:
      - Tracks connection rate per IP
      - Blocks IPs that exceed a certain threshold
      - Automatically unblocks IPs after a block_time
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

        # Data structure to store: { ip: [(timestamp1, timestamp2, ...)], ...}
        self.connection_log = {}

        # Store blocked IP: { ip: unblock_timestamp }
        self.blocked_ips = {}

    def is_blocked(self, ip):
        """Check if IP is currently blocked."""
        current_time = time.time()
        if ip in self.blocked_ips:
            if current_time >= self.blocked_ips[ip]:
                # Unblock IP
                del self.blocked_ips[ip]
                return False
            return True
        return False

    def check_connection(self, ip):
        """
        Checks connection frequency from an IP.
        Updates logs and decides if the connection is allowed or blocked.
        Returns True if allowed, False if blocked.
        """
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
            # Block IP
            self.blocked_ips[ip] = current_time + self.block_time
            print(f"[FIREWALL] Blocking IP {ip} for {self.block_time} seconds (Rate={current_rate} > {self.block_threshold}).")
            return False

        if current_rate > self.rate_limit:
            print(f"[FIREWALL] Warning: IP {ip} is exceeding the soft rate limit (Rate={current_rate}).")

        return True
