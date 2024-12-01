# Format to run code: python DetectPhishing.py <URL_To_Check> <output_file>
import os
import sys
import requests
import time
import json
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# VirusTotal API key from .env file
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

# VirusTotal API endpoints
SCAN_URL_API = "https://www.virustotal.com/vtapi/v2/url/scan"
REPORT_URL_API = "https://www.virustotal.com/vtapi/v2/url/report"
WHOIS_API = "https://www.virustotal.com/vtapi/v2/domain/report"

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class VirusTotalScanner:
    def __init__(self, api_key):
        self.api_key = api_key

    def scan_url(self, url):
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
                logging.error("Error submitting the URL for scanning.")
                return None
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            return None

    def get_url_report(self, scan_id, output_file):
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
                    logging.info("Scan results not ready yet, waiting 15 seconds...")
                    time.sleep(15)
        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")

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
            with open(output_file, "a") as file:
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

    def run(self):
        if len(sys.argv) < 3:
            logging.error("Usage: python DetectPhishing.py <URL> <output_file>")
            sys.exit(1)

        url = sys.argv[1]
        output_file = sys.argv[2]
        domain = url.split("//")[-1].split("/")[0]
        output_file = os.path.join(os.getcwd(), output_file)

        scan_id = self.scanner.scan_url(url)
        if scan_id:
            self.scanner.get_url_report(scan_id, output_file)
        self.scanner.get_whois_info(domain, output_file)


if __name__ == "__main__":
    app = URLScannerApp()
    app.run()
