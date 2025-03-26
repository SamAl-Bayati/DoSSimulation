import socket
import threading
import time
import sys

def handle_client(client_socket, client_address, firewall):
    ip = client_address[0]
    connection_allowed = False
    try:
        # If blocked, do not increment or do anything
        if firewall.is_blocked(ip):
            print(f"[SERVER] Connection from blocked IP {ip} refused.")
            return

        allowed = firewall.check_connection(ip)
        if not allowed:
            print(f"[SERVER] Connection from IP {ip} blocked due to rate limits.")
            return

        # If we reach here, the connection was allowed
        connection_allowed = True

        data = client_socket.recv(1024)
        if data:
            client_socket.sendall(b"Hello from server!\n")

    except Exception as e:
        pass
    finally:
        client_socket.close()
        # Decrement active_connections only if it was allowed
        if connection_allowed:
            firewall.end_connection(ip)

def run_tcp_server(host='0.0.0.0', port=9999, firewall=None):
    print(f"[INFO] Starting TCP server on {host}:{port}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except Exception:
        pass
    server.bind((host, port))
    server.listen(128)
    print("[INFO] Server listening for connections...")

    while True:
        try:
            client_socket, client_address = server.accept()
            total_connections = firewall.active_connections

            # Optional: Crash simulation if mitigations are disabled
            if not firewall.mitigation_enabled and total_connections > 100:
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
            print("[ERROR]", e)
            break
