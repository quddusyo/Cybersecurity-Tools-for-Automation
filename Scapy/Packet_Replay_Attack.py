#Packet Replay Attack to send a custom packet to devices on network using Scapy
from scapy.all import *

# Assume we've captured a TCP SYN packet earlier
captured_packet = IP(dst="10.0.0.137") / TCP(dport=80, flags="S")

# Replay the captured packet
send(captured_packet)
