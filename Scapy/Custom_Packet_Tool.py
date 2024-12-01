'''
Python script to send a single packet to a destination IP and port using Scapy
'''

from scapy.all import *

# Create a TCP packet to port 80 (HTTP)
packet = IP(dst="10.0.0.137") / TCP(dport=80) # Change IP and protocol and destination port as desired
print(packet.show())
# Send the packet and wait for a response
response = sr1(packet)

print("\nResponse from send(): ")
# Check if a response was received
if response is not None:
    print(response.summary())
else:
    print("No response received.")
