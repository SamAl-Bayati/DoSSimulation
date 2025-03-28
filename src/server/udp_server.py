import socket
import time

def run_udp_server(host='0.0.0.0', port=9999, firewall=None):
    """
    A simple UDP server that receives packets on (host, port).
    - If not blocked, calls firewall.record_udp_packet() 
    - Increments firewall.active_connections by check_connection()
    - Then ends the connection after a brief sleep (optional).
    """
    print(f"[INFO] Starting UDP server on {host}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print("[INFO] UDP server listening for packets...")

    while True:
        try:
            data, addr = sock.recvfrom(2048)
            ip = addr[0]

            # 1) If IP is blocked, skip
            if firewall.is_blocked(ip):
                print(f"[SERVER-UDP] Packet from blocked IP {ip} discarded.")
                continue

            # 2) Normal firewall check
            allowed = firewall.check_connection(ip)
            if not allowed:
                print(f"[SERVER-UDP] Packet from IP {ip} blocked by firewall.")
                continue

            # 3) Record a UDP packet timestamp for PPS calculation
            firewall.record_udp_packet()

            # 4) (Optional) do something with 'data'
            print(f"[SERVER-UDP] Received {len(data)} bytes from {ip}")

            # 5) If you want to see a small 'active connection' spike, hold ~0.1s
            time.sleep(0.1)

            # 6) End the "connection"
            firewall.end_connection(ip)

        except KeyboardInterrupt:
            print("\n[INFO] Shutting down UDP server.")
            sock.close()
            break
        except Exception as e:
            print("[ERROR] UDP server exception:", e)
            break
