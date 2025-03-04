import time
import threading
import matplotlib.pyplot as plt
import random

"""
A simple monitor that simulates or reads relevant data.
In a more advanced tool, you would gather metrics from the Firewall or the Server
(e.g., via shared memory, logs, or a messaging system).
Here, we just simulate random data for demonstration.
"""

def fetch_metrics():
    """
    Mock function to simulate fetching metrics about current connections, blocked IPs, etc.
    In a real implementation, you'd retrieve actual data from the Firewall object or server logs.
    """
    # Example structure: return (current_connections, blocked_ips)
    current_connections = random.randint(0, 20)
    blocked_ips = random.randint(0, 5)
    return current_connections, blocked_ips

def start_monitor():
    print("[INFO] Starting real-time monitor... Press Ctrl+C to stop.")
    plt.ion()

    fig, ax = plt.subplots()
    fig.suptitle("DoS Simulation Monitor")

    times = []
    connection_rates = []
    blocked_counts = []

    start_time = time.time()

    while True:
        try:
            now = time.time() - start_time
            current_connections, blocked_ips = fetch_metrics()

            times.append(now)
            connection_rates.append(current_connections)
            blocked_counts.append(blocked_ips)

            ax.clear()
            ax.plot(times, connection_rates, label='Current Connections')
            ax.plot(times, blocked_counts, label='Blocked IPs', color='red')

            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Count")
            ax.set_title("Real-Time Attack / Defense Metrics")
            ax.legend()

            plt.pause(1.0)  # Update plot every second
        except KeyboardInterrupt:
            print("\n[INFO] Stopping monitor.")
            break
    plt.ioff()
    plt.show()
