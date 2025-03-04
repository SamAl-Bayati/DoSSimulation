import socket
import threading
import time

def handle_client(client_socket, client_address, firewall):
    """
    Handles an incoming client connection.
    If the IP is blocked or rate limit is exceeded, we close the connection.
    Otherwise, we simulate some simple echo or hold.
    """
    ip = client_address[0]

    if firewall.is_blocked(ip):
        print(f"[SERVER] Connection from blocked IP {ip} refused.")
        client_socket.close()
        return

    allowed = firewall.check_connection(ip)
    if not allowed:
        print(f"[SERVER] Connection from IP {ip} blocked due to rate limits.")
        client_socket.close()
        return

    try:
        # Simulate a simple echo server
        data = client_socket.recv(1024)
        if data:
            client_socket.sendall(b"Hello from server!\n")
    except:
        pass
    finally:
        client_socket.close()

def run_tcp_server(host='0.0.0.0', port=9999, firewall=None):
    print(f"[INFO] Starting TCP server on {host}:{port}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(128)

    print("[INFO] Server listening for connections...")
    while True:
        try:
            client_socket, client_address = server.accept()
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
            continue
