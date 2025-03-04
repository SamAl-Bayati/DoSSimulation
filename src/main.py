import threading
import time
import sys

from ui.app import app, socketio
from server.tcp_server import run_tcp_server
from monitor.monitor import Monitor
from defender.firewall import Firewall
from attacker.syn_flood import syn_flood
from attacker.udp_flood import udp_flood
from attacker.http_flood import http_flood

# Shared Firewall instance
firewall = Firewall(rate_limit=30, block_threshold=50, block_time=60)

# Shared Monitor instance
monitor = Monitor(firewall)

def start_flask_app():
    # Run Flask app with SocketIO
    socketio.run(app, host='0.0.0.0', port=5000)

def start_tcp_server():
    run_tcp_server(host='0.0.0.0', port=9999, firewall=firewall)

def start_monitor():
    monitor.run()

def main():
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    print("[INFO] Flask web server started on http://0.0.0.0:5000")

    # Start TCP server in a separate thread
    server_thread = threading.Thread(target=start_tcp_server)
    server_thread.daemon = True
    server_thread.start()
    print("[INFO] TCP server started on port 9999")

    # Start Monitor in a separate thread
    monitor_thread = threading.Thread(target=start_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    print("[INFO] Monitor started")

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        sys.exit(0)

if __name__ == '__main__':
    main()
