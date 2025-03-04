from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import threading
import time

# Attack modules
from attacker.syn_flood import syn_flood
from attacker.udp_flood import udp_flood
from attacker.http_flood import http_flood

# Import the shared instances (instead of from main)
from shared import firewall, monitor

app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

# Dictionary to keep track of running attacks
active_attacks = {}

@app.route('/')
def index():
    # Pass firewall so the template can reference firewall.rate_limit, etc.
    return render_template('index.html', firewall=firewall)

@app.route('/start_attack', methods=['POST'])
def start_attack():
    attack_type = request.form.get('attack_type')
    target_ip = request.form.get('target_ip', '127.0.0.1')
    target_port = int(request.form.get('target_port', 9999))
    duration = int(request.form.get('duration', 10))
    rate = int(request.form.get('rate', 100))

    if attack_type in active_attacks:
        flash(f"{attack_type.capitalize()} flood is already running.", "warning")
        return redirect(url_for('index'))

    if attack_type == 'syn':
        attack_thread = threading.Thread(target=syn_flood, args=(target_ip, target_port, duration, rate))
    elif attack_type == 'udp':
        attack_thread = threading.Thread(target=udp_flood, args=(target_ip, target_port, duration, rate))
    elif attack_type == 'http':
        attack_thread = threading.Thread(target=http_flood, args=(target_ip, target_port, duration, rate))
    else:
        flash("Invalid attack type selected.", "danger")
        return redirect(url_for('index'))

    attack_thread.start()
    active_attacks[attack_type] = attack_thread
    flash(f"{attack_type.capitalize()} flood started.", "success")
    return redirect(url_for('index'))

@app.route('/stop_attack', methods=['POST'])
def stop_attack():
    attack_type = request.form.get('attack_type')

    if attack_type not in active_attacks:
        flash(f"No active {attack_type} flood found.", "warning")
        return redirect(url_for('index'))

    flash(f"Stopping {attack_type} flood is not implemented.", "info")
    return redirect(url_for('index'))

@app.route('/mitigations', methods=['GET', 'POST'])
def mitigations():
    if request.method == 'POST':
        rate_limit = request.form.get('rate_limit', type=int)
        block_threshold = request.form.get('block_threshold', type=int)
        block_time = request.form.get('block_time', type=int)

        if rate_limit:
            firewall.rate_limit = rate_limit
        if block_threshold:
            firewall.block_threshold = block_threshold
        if block_time:
            firewall.block_time = block_time

        flash("Mitigation settings updated.", "success")
        return redirect(url_for('mitigations'))

    # Pass firewall so mitigations.html can access firewall properties
    return render_template('mitigations.html', firewall=firewall)

@app.route('/enable_mitigation', methods=['POST'])
def enable_mitigation():
    firewall.enable_mitigation()
    flash("Mitigations enabled.", "success")
    return redirect(url_for('index'))

@app.route('/disable_mitigation', methods=['POST'])
def disable_mitigation():
    firewall.disable_mitigation()
    flash("Mitigations disabled.", "warning")
    return redirect(url_for('index'))

@app.route('/monitor')
def monitor_page():
    return render_template('montior.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit_metrics()

def emit_metrics():
    """
    Emit metrics to connected clients every second.
    """
    while True:
        try:
            time.sleep(1)
            metrics = monitor.get_metrics()
            socketio.emit('metrics', metrics)
        except KeyboardInterrupt:
            break

# Start emitting metrics in a background thread
socketio.start_background_task(target=emit_metrics)
