import os
import eventlet
eventlet.monkey_patch()

import threading
import time
import sys

from ui.app import app, socketio
from shared import firewall, monitor
from server.tcp_server import run_tcp_server

def start_tcp_server():
    run_tcp_server(host='0.0.0.0', port=9999, firewall=firewall)

def start_monitor():
    monitor.run()

def main():
    # Only start background threads if this is the main process.
    # This avoids duplicate TCP server instantiation in reloader/debug modes.
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get("WERKZEUG_RUN_MAIN") is None:
        tcp_thread = threading.Thread(target=start_tcp_server)
        tcp_thread.daemon = True
        tcp_thread.start()
        print("[INFO] TCP server started on port 9999")

        monitor_thread = threading.Thread(target=start_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        print("[INFO] Monitor started")
    
    print("[INFO] Starting Flask web server on http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    main()
