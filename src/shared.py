from defender.firewall import Firewall
from monitor.monitor import Monitor

firewall = Firewall(rate_limit=30, block_threshold=50, block_time=60)
monitor = Monitor(firewall)

server_status = {
    'crashed': False,
    'message': None
}
