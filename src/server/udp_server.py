import socket
import time

def run_udp_server(host='0.0.0.0', port=9999, firewall=None):
    """
    A simple UDP server that receives packets on (host, port).
    Each packet is 'checked' by the firewall, artificially increments
    active_connections for ~0.5s so the real-time chart can see it,
    and then calls end_connection().
    """
    print(f"[INFO] Starting UDP server on {host}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print("[INFO] UDP server listening for packets...")

    while True:
        try:
            data, addr = sock.recvfrom(2048)
            ip = addr[0]

            # 1) If IP is already blocked, skip
            if firewall.is_blocked(ip):
                print(f"[SERVER-UDP] Packet from blocked IP {ip} discarded.")
                # This increments denied_connections internally
                continue

            # 2) Normal firewall check
            allowed = firewall.check_connection(ip)
            if not allowed:
                print(f"[SERVER-UDP] Packet from IP {ip} blocked by firewall.")
                continue

            # 3) If allowed, do something with 'data'
            print(f"[SERVER-UDP] Received {len(data)} bytes from {ip}")

            # Artificially hold the "connection" so the real-time chart can see the increment.
            # If we skip this delay, the connection will end so fast that the chart rarely
            # shows anything but 0.
            time.sleep(0.5)

            # 4) End the connection
            firewall.end_connection(ip)

        except KeyboardInterrupt:
            print("\n[INFO] Shutting down UDP server.")
            sock.close()
            break
        except Exception as e:
            print("[ERROR] UDP server exception:", e)
            break
