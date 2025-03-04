# DoSSimulation

This project is for **educational** purposes only. It demonstrates how Denial of Service (DoS) attacks can be simulated in a controlled environment, and shows basic defense mechanisms like rate limiting and IP blocking.

## Features

- **Attacks**:
  - SYN flood
  - UDP flood
  - HTTP GET flood
- **Server**:
  - Simple TCP server to simulate a vulnerable service
- **Defense**:
  - Basic firewall with rate limiting and IP blacklisting
- **Monitoring**:
  - Track connection rates and blocked IP addresses
  - Real-time visualization with Matplotlib

## Usage

```bash
# Install requirements
pip install -r requirements.txt

# Launch the server (in one terminal)
python src/main.py server --port 9999

# Start the monitor (in a second terminal)
python src/main.py monitor

# Launch an attack (in a third terminal)
python src/main.py attack --type syn --target 127.0.0.1 --port 9999 --duration 10
