# DoSSimulation

This project is for **educational** purposes only. It demonstrates how Denial of Service (DoS) attacks can be simulated in a controlled environment and shows basic defense mechanisms like rate limiting and IP blocking.

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
  - Real-time visualization of connection rates and blocked IPs via a web interface

## Usage

1. **clone repo and move to it** (recommended to use a virtual environment):
    ```bash
    git clone https://github.com/SamAl-Bayati/DoSSimulation.git
    cd DoSSimulation
    ```

2. **Run the application**:
    ```bash
    sudo ./run.sh
    ```

3. **Access the web interface**:
    - Open your browser and navigate to [http://localhost:5000](http://localhost:5000)

4. **Interact with the UI**:
    - **Launch Attacks**: Select attack type, target IP, port, duration, and rate to start an attack.
    - **Mitigation Controls**: Enable or disable mitigation strategies and adjust settings.
    - **Real-Time Monitor**: View ongoing metrics about connections and blocked IPs.

## Important

- **Root Privileges**:  
  - SYN flood attacks typically require raw packet crafting, which usually requires administrator (root) privileges on Unix systems.  
  - If you run into permission errors, try using `sudo`.

- **Legal and Ethical Use**:  
  - This tool should **only** be run against servers or networks that you own or have explicit permission to test.  
  - Do **not** use this on public networks. Unauthorized DoS attacks are illegal in many jurisdictions.

- **Performance and Environment**:  
  - This is a **demo** tool, not optimized for high-performance attacks or real-world defense.  
  - For serious testing, isolate your environment (e.g., local VMs or test lab).
