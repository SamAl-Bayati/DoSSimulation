import eventlet
eventlet.monkey_patch()

import threading
import time
import sys

# Import the Flask app and SocketIO from app.py
from ui.app import app, socketio

# Import the shared instances from shared.py
from shared import firewall, monitor

# Import server logic
from server.tcp_server import run_tcp_server

def start_tcp_server():
    run_tcp_server(host='0.0.0.0', port=9999, firewall=firewall)

def start_monitor():
    monitor.run()

def main():
    # Start the TCP server in a background thread
    tcp_thread = threading.Thread(target=start_tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()
    print("[INFO] TCP server started on port 9999")

    # Start the Monitor in a background thread
    monitor_thread = threading.Thread(target=start_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    print("[INFO] Monitor started")

    # Now, run the Flask server in the main thread with the reloader disabled
    print("[INFO] Starting Flask web server on http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == '__main__':
    main()
