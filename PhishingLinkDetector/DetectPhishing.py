'''
Author: Yousuf A. Quddus
Description: Script which takes a URL input & output filename. The script then checks through various tests
to determine if the link is a phishing link. The link uses VirusTotals' API for link test scanning alongside
the WHOIS lookup feature and logs it into the output file for futher analysis. The script uses
sandboxing within VM VirtualBox where the link in executed and further analyzed using the users tools of choice. 
The script also creates a log file, DetectPhsihingScanner.log which can be used to analyze captured errors 
and usage integrity in the future.
Usage: python DetectPhishing.py <URL> <output_file>
Example malicious URL found on VirusTotal: www.xmlformats.com 10 out of 96 warnings found.
'''

# Import Libraries
import os
import sys
import subprocess
import requests
import time
import json
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup logging for both console and file outputs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("DetectPhishingScanner.log"),
        logging.StreamHandler()
    ]
)

# VirusTotal API key from .env file
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

# VirtualBox VM configuration
VM_NAME = os.getenv("VM_NAME", "default_VM_Name")  # "default_VM_Name" if not provided in .env
VM_USERNAME = os.getenv("VM_USERNAME", "default_user")  # Default username
VM_PASSWORD = os.getenv("VM_PASSWORD", "default_password")  # Default password

# VirusTotal API endpoints
SCAN_URL_API = "https://www.virustotal.com/vtapi/v2/url/scan"
REPORT_URL_API = "https://www.virustotal.com/vtapi/v2/url/report"
WHOIS_API = "https://www.virustotal.com/vtapi/v2/domain/report"

class VirusTotalScanner:
    def __init__(self, api_key):
        self.api_key = api_key

    def scan_url(self, url):
        """Submits a URL for scanning on VirusTotal."""
        try:
            params = {
                "apikey": self.api_key,
                "url": url,
            }
            logging.info(f"Submitting URL {url} for scanning on VirusTotal...")
            response = requests.post(SCAN_URL_API, data=params)
            response.raise_for_status()
            result = response.json()

            if result.get("response_code") == 1:
                logging.info(f"Scan submitted successfully. Scan ID: {result.get('scan_id')}")
                return result.get("scan_id")
            else:
                logging.error("Error: Unable to submit the URL for scanning.")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error: {e}")
            return None

    def get_url_report(self, scan_id, output_file):
        """Fetches the report for the scanned URL."""
        try:
            params = {
                "apikey": self.api_key,
                "resource": scan_id,
            }
            logging.info(f"Fetching scan report for Scan ID: {scan_id}...")
            while True:
                response = requests.get(REPORT_URL_API, params=params)
                response.raise_for_status()
                result = response.json()
                
                if result.get("response_code") == 1:
                    positives = int(result.get("positives", 0))
                    total = int(result.get("total", 0))
                    logging.info(f"The URL has been flagged by {positives} out of {total} scanners.")
                    
                    with open(output_file, "a+") as file:
                        json.dump(result, file, indent=4)
                    logging.info(f"Report saved to {output_file}")
                    break
                else:
                    logging.info("Scan results not ready yet, waiting 10 seconds...")
                    time.sleep(10)
        except requests.exceptions.RequestException as e:
            logging.error(f"Error, Request failed: {e}")

    def get_whois_info(self, domain, output_file):
        try:
            params = {
                "apikey": self.api_key,
                "domain": domain,
            }
            logging.info(f"Fetching WHOIS information for domain: {domain}...")
            response = requests.get(WHOIS_API, params=params)
            response.raise_for_status()
            result = response.json()
            
            whois_data = result.get("whois", "No WHOIS data available")
            with open(output_file, "a+") as file:
                file.write("\n\nWHOIS Information:\n")
                if isinstance(whois_data, str):
                    file.write(whois_data.replace("\\n", "\n"))
                else:
                    json.dump(whois_data, file, indent=4)
            logging.info(f"WHOIS information saved to {output_file}")
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")

class URLScannerApp:
    def __init__(self):
        self.api_key = API_KEY
        self.scanner = VirusTotalScanner(self.api_key)

    def run(self, url, output_file):
        domain = url.split("//")[-1].split("/")[0]
        output_file = os.path.join(os.getcwd(), output_file)

        scan_id = self.scanner.scan_url(url)
        if scan_id:
            self.scanner.get_url_report(scan_id, output_file)
        self.scanner.get_whois_info(domain, output_file)

def start_virtualbox(vm_name):
    """Starts the specified VirtualBox VM in GUI mode."""
    try:
        print(f"Starting VirtualBox VM: {vm_name}")
        subprocess.run(["VBoxManage", "startvm", vm_name], check=True)
        print(f"VM {vm_name} started successfully.")
    except subprocess.CalledProcessError:
        print("Failed to start the VirtualBox VM. Ensure the VM name is correct.")
        return False
    return True

def login_and_run_sudo(vm_name, url, output_file):
    """Logs in to the VM, opens the default terminal emulator, runs 'sudo su', and enters the password."""
    username = VM_USERNAME
    password = VM_PASSWORD

    print("Waiting for VM to boot...")
    time.sleep(40)  # Wait for the VM to boot (adjust if needed)

    print("Sending username...")
    for char in username + "\n":
        subprocess.run(["VBoxManage", "controlvm", vm_name, "keyboardputstring", char])

    # Simulate pressing tab key to advance to password section
    time.sleep(0.5)
    subprocess.run(["VBoxManage", "controlvm", vm_name, "keyboardputscancode", "0F"])  # Scancode for tab key
    time.sleep(0.2)
    subprocess.run(["VBoxManage", "controlvm", vm_name, "keyboardputscancode", "8F"])  # Scancode for tab key

    print("Sending password...")
    for char in password:
        subprocess.run(["VBoxManage", "controlvm", vm_name, "keyboardputstring", char])

    print("Logging in...")
    # Simulate hitting Enter key to log in
    subprocess.run(["VBoxManage", "controlvm", vm_name, "keyboardputscancode", "1c"])  # Scancode for Enter key
    time.sleep(0.2)
    subprocess.run(["VBoxManage", "controlvm", vm_name, "keyboardputscancode", "9c"])  # Scancode for release Enter key

    time.sleep(5) # Give time for the VM to login (adjust if needed)
    # Execute the phishing detection inside the VM after logging in
    print(f"Opening link for dynamic analysis in {vm_name}...")
    # Send a command to the terminal to open the link you are checking for dynamic analysis
    subprocess.run(["VBoxManage", "controlvm", vm_name, "keyboardputstring", f"firefox {url}\n"])

    scanner_app = URLScannerApp()
    scanner_app.run(url, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python combined_script.py <URL_To_Check> <output_file>")
        sys.exit(1)

    url_to_check = sys.argv[1]
    output_file = sys.argv[2]
 
    if start_virtualbox(VM_NAME):
        login_and_run_sudo(VM_NAME, url_to_check, output_file)
