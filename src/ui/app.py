from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import threading
import time
import logging
import eventlet
eventlet.monkey_patch()

from attacker.syn_flood import syn_flood
from attacker.udp_flood import udp_flood
from attacker.http_flood import http_flood
from shared import firewall, monitor

logging.basicConfig(level=logging.DEBUG)

# Use the templates folder in the same directory
app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'
socketio = SocketIO(app, logger=True, engineio_logger=True)

@app.before_request
def before_request():
    app.logger.debug("Incoming request: %s %s", request.method, request.url)

@app.after_request
def after_request(response):
    app.logger.debug("Response status: %s", response.status)
    return response

active_attacks = {}

@app.route('/')
def index():
    app.logger.debug("Index route accessed.")
    return render_template('index.html', firewall=firewall)

@app.route('/start_attack', methods=['POST'])
def start_attack():
    """
    Launch a single attacker thread that runs the chosen DoS method.
    """
    app.logger.debug("Start attack route accessed.")
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
        return redirect(url_for('index'))

    t.start()
    app.logger.debug("Started attack thread: %s", t.name)
    active_attacks[attack_type] = t
    flash(f"{attack_type.capitalize()} flood started.", "success")
    return redirect(url_for('monitor_page'))

@app.route('/stop_attack', methods=['POST'])
def stop_attack():
    """
    Stub: stopping the flood isn't currently implemented in your code,
    because each attacker is just a simple function that ends after 'duration'.
    """
    app.logger.debug("Stop attack route accessed.")
    attack_type = request.form.get('attack_type')
    if attack_type not in active_attacks:
        flash(f"No active {attack_type} flood found.", "warning")
        return redirect(url_for('index'))
    flash(f"Stopping {attack_type} flood is not implemented.", "info")
    return redirect(url_for('index'))

@app.route('/mitigations', methods=['GET', 'POST'])
def mitigations():
    app.logger.debug("Mitigations route accessed. Method: %s", request.method)
    if request.method == 'POST':
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
        return redirect(url_for('mitigations'))
    return render_template('mitigations.html', firewall=firewall)

@app.route('/enable_mitigation', methods=['POST'])
def enable_mitigation():
    app.logger.debug("Enable mitigation route accessed.")
    firewall.enable_mitigation()
    flash("Mitigations enabled.", "success")
    return redirect(url_for('index'))

@app.route('/disable_mitigation', methods=['POST'])
def disable_mitigation():
    app.logger.debug("Disable mitigation route accessed.")
    firewall.disable_mitigation()
    flash("Mitigations disabled.", "warning")
    return redirect(url_for('index'))

@app.route('/monitor')
def monitor_page():
    app.logger.debug("Monitor page accessed.")
    return render_template('monitor.html')

@socketio.on('connect')
def handle_connect():
    app.logger.debug("SocketIO client connected.")

def emit_metrics():
    """
    Runs in the background, emitting metrics to all connected Socket.IO clients once per second.
    """
    app.logger.debug("emit_metrics background task started.")
    while True:
        eventlet.sleep(1)
        try:
            metrics = monitor.get_metrics()
            socketio.emit('metrics', metrics)
            app.logger.debug("Emitted metrics: %s", metrics)
        except Exception as e:
            app.logger.error("Error in emit_metrics: %s", e)
            break

socketio.start_background_task(target=emit_metrics)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
