import socket
import time

def run_udp_server(host='0.0.0.0', port=9999, firewall=None):
    """
    A simple UDP server that receives packets on (host, port).
    Each packet is 'checked' via the firewall logic.
    If blocked, increment denied count.
    If allowed, briefly increments active_connections,
    then calls end_connection() right away to keep the metrics correct.
    """
    print(f"[INFO] Starting UDP server on {host}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print("[INFO] UDP server listening for packets...")

    while True:
        try:
            data, addr = sock.recvfrom(2048)
            ip = addr[0]

            # 1) Is the IP blocked?
            if firewall.is_blocked(ip):
                print(f"[SERVER-UDP] Packet from blocked IP {ip} discarded.")
                # We do NOT call check_connection() or end_connection() if it's already blocked;
                # but if you want to increment 'denied_connections' further, you could do so manually.
                continue

            # 2) Perform normal firewall check
            allowed = firewall.check_connection(ip)
            if not allowed:
                print(f"[SERVER-UDP] Packet from IP {ip} blocked by firewall.")
                continue

            # If allowed, you can do something with 'data' here, or ignore it
            # For demonstration, let's just print how many bytes we got:
            print(f"[SERVER-UDP] Received {len(data)} bytes from {ip}")

            # 3) Because UDP doesn't have an actual "connection" to close, 
            #    we immediately call end_connection() so active_connections won't stay high forever.
            firewall.end_connection(ip)

        except KeyboardInterrupt:
            print("\n[INFO] Shutting down UDP server.")
            sock.close()
            break
        except Exception as e:
            print("[ERROR] UDP server exception:", e)
            break
