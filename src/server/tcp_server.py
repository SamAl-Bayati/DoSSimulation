import socket
import threading
import time
import sys
import shared

def handle_client(client_socket, client_address, firewall):
    ip = client_address[0]

    if firewall.is_blocked(ip):
        print(f"[SERVER] Connection from blocked IP {ip} refused.")
        client_socket.close()
        return

    allowed = firewall.check_connection(ip)
    if not allowed:
        print(f"[SERVER] Connection from IP {ip} blocked due to firewall mitigation.")
        client_socket.close()
        return

    try:
        data = client_socket.recv(1024)
        if data:
            client_socket.sendall(b"Hello from server!\n")
        time.sleep(1)
    except:
        pass
    finally:
        client_socket.close()
        firewall.end_connection(ip)

def run_tcp_server(host='0.0.0.0', port=9999, firewall=None):
    """
    Restarts automatically if it crashes.
    """
    while True:
        shared.server_status['crashed'] = False
        shared.server_status['message'] = None

        try:
            print(f"[INFO] Starting TCP server on {host}:{port}")
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except:
                pass
            server.bind((host, port))
            server.listen(128)
            print("[INFO] Server listening for connections...")

            while True:
                client_socket, client_address = server.accept()
                if not firewall.mitigation_enabled and firewall.active_connections > 100:
                    print("[CRASH] Too many connections! Server is crashing.")
                    raise Exception("Server Crash: Overwhelmed by connections")

                handler = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address, firewall)
                )
                handler.daemon = True
                handler.start()

        except KeyboardInterrupt:
            print("\n[INFO] Shutting down server.")
            server.close()
            break
        except Exception as e:
            print("[ERROR] Server crashed:", e)
            shared.server_status['crashed'] = True
            shared.server_status['message'] = str(e)
            firewall.reset_caches()
            print("[INFO] Restarting server in 2 seconds...")
            time.sleep(2)
            continue
