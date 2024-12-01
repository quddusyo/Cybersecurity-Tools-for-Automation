'''
Python script to check whether a (checks one port) port is open or closed given an IP address.
'''
# Script Format:
# python port_scanner.py <IP> <Port>
import socket
import sys

def port_scanner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout of 1 second

        result = sock.connect_ex((ip, port))
        
        if result == 0:
            print(f"Port {port} is OPEN on {ip}")
        else:
            print(f"Port {port} is CLOSED on {ip}")
        
        sock.close()
    except socket.error as e:
        print(f"Error: {e}")
        sys.exit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python port_scanner.py <IP> <Port>")
        sys.exit()

    ip_address = sys.argv[1]
    port = int(sys.argv[2])

    print(f"Scanning port {port} on IP {ip_address}...")
    port_scanner(ip_address, port)
