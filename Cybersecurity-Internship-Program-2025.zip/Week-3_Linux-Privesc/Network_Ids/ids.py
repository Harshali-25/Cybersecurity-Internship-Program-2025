import sys
from scapy.all import rdpcap, IP, ICMP, TCP
from collections import defaultdict

icmp_count = defaultdict(int)
syn_count = defaultdict(int)

# ----------- ICMP Detection -----------
def detect_icmp(pkt):
    if pkt.haslayer(ICMP):
        if pkt[ICMP].type == 8:  # Echo Request (Ping)
            src = pkt[IP].src
            dst = pkt[IP].dst
            icmp_count[src] += 1
            print(f"[ICMP] Ping from {src} to {dst}")

            if icmp_count[src] > 5:
                print(f"[ALERT] Possible ICMP flood from {src}")

# ----------- TCP Detection -----------
def detect_tcp(pkt):
    if pkt.haslayer(TCP):
        flags = pkt[TCP].flags
        src = pkt[IP].src
        dst = pkt[IP].dst
        dport = pkt[TCP].dport

        if flags == "S":  # SYN
            syn_count[src] += 1
            print(f"[TCP] SYN attempt from {src} to {dst}:{dport}")
            if syn_count[src] > 10:
                print(f"[ALERT] Possible SYN scan/flood from {src}")

        elif flags == 0:  # NULL scan
            print(f"[TCP] NULL scan detected from {src} to {dst}:{dport}")

        elif flags == "F":  # FIN scan
            print(f"[TCP] FIN scan detected from {src} to {dst}:{dport}")

# ----------- Analyze PCAP File -----------
def analyze_pcap(filename):
    print(f"\n[+] Analyzing {filename} ...\n")
    packets = rdpcap(filename)
    for pkt in packets:
        if pkt.haslayer(IP):
            detect_icmp(pkt)
            detect_tcp(pkt)

# ----------- Main Program -----------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ids.py <pcapfile>")
    else:
        pcap_file = sys.argv[1]
        analyze_pcap(pcap_file)
