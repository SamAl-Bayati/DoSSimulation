from defender.firewall import Firewall
from monitor.monitor import Monitor

# Create the Firewall instance
firewall = Firewall(rate_limit=30, block_threshold=50, block_time=60)

# Create the Monitor instance that depends on the firewall
monitor = Monitor(firewall)
