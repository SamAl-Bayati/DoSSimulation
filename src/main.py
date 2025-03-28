import os
import eventlet
eventlet.monkey_patch()
import threading
import time
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

from ui.app import app, socketio
from shared import firewall, monitor
from server.tcp_server import run_tcp_server
from server.udp_server import run_udp_server

def start_tcp_server():
    logging.info("Starting TCP server thread...")
    run_tcp_server(host='0.0.0.0', port=9999, firewall=firewall)

def start_udp_server():
    logging.info("Starting UDP server thread...")
    run_udp_server(host='0.0.0.0', port=9999, firewall=firewall)

def start_monitor():
    logging.info("Starting monitor thread...")
    monitor.run()

def main():
    logging.info("Main process starting. WERKZEUG_RUN_MAIN=%s", os.environ.get("WERKZEUG_RUN_MAIN"))

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or os.environ.get("WERKZEUG_RUN_MAIN") is None:
        tcp_thread = threading.Thread(target=start_tcp_server)
        tcp_thread.daemon = True
        tcp_thread.start()
        logging.info("TCP server thread started.")

        udp_thread = threading.Thread(target=start_udp_server)
        udp_thread.daemon = True
        udp_thread.start()
        logging.info("UDP server thread started.")

        monitor_thread = threading.Thread(target=start_monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        logging.info("Monitor thread started.")
    
    logging.info("Starting Flask web server on http://0.0.0.0:5000")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    logging.info("Flask web server has stopped.")

if __name__ == '__main__':
    main()
