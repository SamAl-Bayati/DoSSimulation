import argparse
import sys

from attacker.syn_flood import syn_flood
from attacker.udp_flood import udp_flood
from attacker.http_flood import http_flood
from server.tcp_server import run_tcp_server
from monitor.monitor import start_monitor

def main():
    parser = argparse.ArgumentParser(
        description="DoS Attack Simulation & Mitigation Tool"
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Server command
    server_parser = subparsers.add_parser('server', help='Start the TCP server')
    server_parser.add_argument('--port', type=int, default=9999, help='Port to run the server on')
    server_parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the server')

    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Start the monitoring tool')
    # No special arguments here, but you can add if needed

    # Attack command
    attack_parser = subparsers.add_parser('attack', help='Launch a DoS attack')
    attack_parser.add_argument('--type', type=str, required=True, choices=['syn', 'udp', 'http'],
                               help='Type of DoS attack (syn, udp, http)')
    attack_parser.add_argument('--target', type=str, default='127.0.0.1', help='Target IP/Host')
    attack_parser.add_argument('--port', type=int, default=80, help='Target Port')
    attack_parser.add_argument('--duration', type=int, default=10, help='Attack duration in seconds')
    attack_parser.add_argument('--rate', type=int, default=100, help='Approx. packets/sec or requests/sec')

    args = parser.parse_args()

    if args.command == 'server':
        run_tcp_server(host=args.host, port=args.port)
    elif args.command == 'monitor':
        start_monitor()
    elif args.command == 'attack':
        if args.type == 'syn':
            syn_flood(args.target, args.port, args.duration, args.rate)
        elif args.type == 'udp':
            udp_flood(args.target, args.port, args.duration, args.rate)
        elif args.type == 'http':
            http_flood(args.target, args.port, args.duration, args.rate)
    else:
        parser.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting... (Keyboard Interrupt)")
        sys.exit(0)
