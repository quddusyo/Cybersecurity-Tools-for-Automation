'''
Python script to scan UDP on a IP Scanning using UDP and Scapy module.
'''

from scapy.all import *

def udp_scan(target, ports):
    print(f"Scanning {target} for open UDP ports...")
    for port in ports:
        packet = IP(dst=target) / UDP(dport=port)
        response = sr1(packet, timeout=2, verbose=0)
        
        if not response:
            print(f"Port {port} is open or filtered (no response).")
        elif response.haslayer(ICMP):
            print(f"Port {port} is closed (ICMP unreachable).")

# Scan UDP ports 53 (DNS) and 67 (DHCP) (can add more ports as desired)
target_ip = "8.8.8.8" # Change IP to desired IP
udp_scan(target_ip, [53, 67])
