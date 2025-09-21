from scapy.all import *
import time
import re
from collections import defaultdict, deque

# Track packets
icmp_counts = defaultdict(lambda: deque())
blocked_ips = {}

# Block rules
ICMP_LIMIT = 10   # max ICMP per second
BLOCK_TIME = 60   # seconds

SQLI_REGEX = re.compile(rb"(union\s+select|or\s+1=1|--)", re.I)

def is_blocked(ip):
    if ip in blocked_ips and blocked_ips[ip] > time.time():
        return True
    return False

def block_ip(ip, sec=BLOCK_TIME):
    blocked_ips[ip] = time.time() + sec
    print(f"[BLOCK] {ip} for {sec}s")

def process_packet(pkt):
    if pkt.haslayer(IP):
        src = pkt[IP].src

        # Check ICMP flood
        if pkt.haslayer(ICMP):
            icmp_counts[src].append(time.time())
            while icmp_counts[src] and icmp_counts[src][0] < time.time() - 1:
                icmp_counts[src].popleft()
            if len(icmp_counts[src]) > ICMP_LIMIT:
                block_ip(src)
                return True

        # Check suspicious payload
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            data = bytes(pkt[Raw])
            if SQLI_REGEX.search(data):
                block_ip(src, 120)
                return True
    return False

# Offline mode: read from pcap
def run_pcap(file):
    for pkt in PcapReader(file):
        if process_packet(pkt):
            print(f"[BLOCKED] {pkt.summary()}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        run_pcap(sys.argv[1])
    else:
        print("Usage: sudo python3 mini_ips.py <file.pcap>")
