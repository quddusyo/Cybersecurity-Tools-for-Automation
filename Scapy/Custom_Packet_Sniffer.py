'''
Python script for Sniffing & Traffic Analysis using Scapy library.
Captures packets from destination IP to host IP alongside ports involved.
'''

from scapy.all import *

def packet_sniffer(packet):
    # Check if packet has IP layer and TCP layer
    if packet.haslayer(IP) and packet.haslayer(TCP):
        print(f"Captured IP Packet: {packet[IP].src} -> {packet[IP].dst}")
        print(f"TCP Source Port: {packet[TCP].sport}, Destination Port: {packet[TCP].dport}")

# Sniff 10 packets, filtering only for TCP
sniff(filter="tcp", prn=packet_sniffer, count=10) # Modify count to number of packets desired
