import socket
import time

def run_udp_server(host='0.0.0.0', port=9999, firewall=None):
    """
    Receives UDP packets, checks firewall, tracks packets for PPS, ends each 'connection' after a brief pause.
    """
    print(f"[INFO] Starting UDP server on {host}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print("[INFO] UDP server listening for packets...")

    while True:
        try:
            data, addr = sock.recvfrom(2048)
            ip = addr[0]

            if firewall.is_blocked(ip):
                print(f"[SERVER-UDP] Packet from blocked IP {ip} discarded.")
                continue

            allowed = firewall.check_connection(ip)
            if not allowed:
                print(f"[SERVER-UDP] Packet from IP {ip} blocked by firewall.")
                continue

            firewall.record_udp_packet()
            print(f"[SERVER-UDP] Received {len(data)} bytes from {ip}")
            time.sleep(0.1)
            firewall.end_connection(ip)

        except KeyboardInterrupt:
            print("\n[INFO] Shutting down UDP server.")
            sock.close()
            break
        except Exception as e:
            print("[ERROR] UDP server exception:", e)
            break
