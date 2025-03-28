import threading
import eventlet
import time
import logging

eventlet.monkey_patch()

from flask import Flask, render_template, request, flash
from flask_socketio import SocketIO, emit
from attacker.syn_flood import syn_flood
from attacker.udp_flood import udp_flood
from attacker.http_flood import http_flood
from shared import firewall, monitor

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, logger=True, engineio_logger=True)

active_attacks = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Single page that:
      - Displays real-time charts
      - Displays mitigation forms
      - Displays the "start attack" form
      - Has a "clear cache" button
      - Processes form submissions (POST)
    """
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_mitigation':
            rate_limit = request.form.get('rate_limit', type=int)
            block_threshold = request.form.get('block_threshold', type=int)
            block_time = request.form.get('block_time', type=int)
            if rate_limit is not None:
                firewall.rate_limit = rate_limit
            if block_threshold is not None:
                firewall.block_threshold = block_threshold
            if block_time is not None:
                firewall.block_time = block_time
            flash("Mitigation settings updated.", "success")

        elif action == 'enable_mitigation':
            firewall.enable_mitigation()
            flash("Mitigations enabled.", "success")

        elif action == 'disable_mitigation':
            firewall.disable_mitigation()
            flash("Mitigations disabled.", "warning")

        elif action == 'clear_cache':
            firewall.reset_caches()
            flash("Firewall caches/logs cleared.", "info")

        elif action == 'start_attack':
            attack_type = request.form.get('attack_type')
            target_ip = request.form.get('target_ip', '127.0.0.1')
            target_port = int(request.form.get('target_port', 9999))
            duration = int(request.form.get('duration', 10))
            rate = int(request.form.get('rate', 100))

            if attack_type == 'syn':
                t = threading.Thread(target=syn_flood, args=(target_ip, target_port, duration, rate))
            elif attack_type == 'udp':
                t = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration, rate))
            elif attack_type == 'http':
                t = threading.Thread(target=http_flood, args=(target_ip, target_port, duration, rate))
            else:
                flash("Invalid attack type selected.", "danger")
                return render_template('index.html', firewall=firewall)

            t.start()
            active_attacks[attack_type] = t
            flash(f"{attack_type.upper()} flood started.", "success")

    return render_template('index.html', firewall=firewall)


@socketio.on('connect')
def handle_connect():
    app.logger.debug("SocketIO client connected.")


def emit_metrics():
    """
    Background thread to emit firewall/monitor metrics every 1s.
    """
    while True:
        eventlet.sleep(1)
        try:
            metrics = monitor.get_metrics()
            socketio.emit('metrics', metrics)
        except Exception as e:
            app.logger.error("Error in emit_metrics: %s", e)
            break

# Start sending metrics in the background
socketio.start_background_task(target=emit_metrics)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
