#!/usr/bin/env bash

# Example usage script

# Install dependencies
pip install -r requirements.txt

# Start the server on port 9999
python src/main.py server --port 9999 &
SERVER_PID=$!
echo "Server started with PID $SERVER_PID"

# Start the monitoring tool
python src/main.py monitor &
MONITOR_PID=$!
echo "Monitor started with PID $MONITOR_PID"

# Launch a 10-second SYN flood attack
python src/main.py attack --type syn --target 127.0.0.1 --port 9999 --duration 10

# Kill the server and monitor
kill $SERVER_PID
kill $MONITOR_PID
echo "Server and monitor stopped."
