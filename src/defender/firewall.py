import time

class Firewall:
    def __init__(self, rate_limit=30, block_threshold=50, block_time=60):
        self.rate_limit = rate_limit
        self.block_threshold = block_threshold
        self.block_time = block_time

        # Logs and counters
        self.connection_log = {}   # { ip: [timestamps of connections in the last minute] }
        self.blocked_ips = {}      # { ip: unblock_time }
        self.mitigation_enabled = True

        # Active live connections right now
        self.active_connections = 0

        # Rolling denies (store timestamps for the last 60s)
        self.denied_threshold_log = []
        self.denied_block_log = []

    def enable_mitigation(self):
        self.mitigation_enabled = True
        print("[FIREWALL] Mitigations enabled.")

    def disable_mitigation(self):
        self.mitigation_enabled = False
        print("[FIREWALL] Mitigations disabled.")

    def prune_expired_blocks(self):
        """
        Remove IPs from block list if their block_time has expired.
        This ensures that even if the IP does not reconnect,
        the block will be lifted automatically.
        """
        current_time = time.time()
        to_remove = []
        for ip, unblock_time in self.blocked_ips.items():
            if current_time >= unblock_time:
                to_remove.append(ip)
        for ip in to_remove:
            del self.blocked_ips[ip]

    def is_blocked(self, ip):
        """
        Checks if the IP is currently blocked, removing it from the list
        if the block time has expired. If it is still blocked, log the denial.
        """
        self.prune_expired_blocks()
        if ip in self.blocked_ips:
            # IP is still actively blocked
            self.denied_block_log.append(time.time())  # Rolling window
            return True
        return False

    def check_connection(self, ip):
        """
        Checks if the connection from ip is allowed under the current mitigation rules.
        If blocked by threshold, log that deny and block the IP for block_time.
        If the IP is allowed, increment active_connections.
        """
        if not self.mitigation_enabled:
            # Mitigation is off, just increment active
            self.active_connections += 1
            return True

        # Mitigation is on. First, prune old entries for this IP.
        current_time = time.time()
        one_minute_ago = current_time - 60
        if ip not in self.connection_log:
            self.connection_log[ip] = []
        # Remove old timestamps for that IP
        self.connection_log[ip] = [ts for ts in self.connection_log[ip] if ts > one_minute_ago]

        # Record this new connection
        self.connection_log[ip].append(current_time)

        current_rate = len(self.connection_log[ip])
        # If above threshold, block immediately
        if current_rate > self.block_threshold:
            # Block this IP for block_time
            self.blocked_ips[ip] = current_time + self.block_time
            # Log a threshold deny
            self.denied_threshold_log.append(current_time)
            print(f"[FIREWALL] Blocking IP {ip} for {self.block_time} seconds (Rate={current_rate} > {self.block_threshold}).")
            return False

        # Optionally warn if exceeding soft rate_limit
        if current_rate > self.rate_limit:
            print(f"[FIREWALL] Warning: IP {ip} is exceeding the soft rate limit (Rate={current_rate}).")

        # Allowed
        self.active_connections += 1
        return True

    def end_connection(self, ip):
        """
        Called when a connection closes. Decrement active_connections if > 0.
        """
        if self.active_connections > 0:
            self.active_connections -= 1

    def prune_connection_logs(self):
        """
        Periodically remove old timestamps from all IPs so that
        memory isn't wasted for IPs that won't connect again.
        """
        cutoff = time.time() - 60
        empty_ips = []
        for ip, timestamps in self.connection_log.items():
            new_ts = [t for t in timestamps if t > cutoff]
            if new_ts:
                self.connection_log[ip] = new_ts
            else:
                empty_ips.append(ip)
        for ip in empty_ips:
            del self.connection_log[ip]
