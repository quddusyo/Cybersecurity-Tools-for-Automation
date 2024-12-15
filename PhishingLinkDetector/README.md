# DetectPhishing.py

## Author  
**Yousuf A. Quddus**

## Description  
`DetectPhishing.py` is a Python script designed to analyze URLs for phishing activity. It integrates with the **VirusTotal API** to perform URL scans, fetch WHOIS information, and log the results. Additionally, it utilizes **VirtualBox** for sandboxed URL execution, allowing for dynamic analysis using user-specified tools. Logs are generated to ensure transparency and integrity.

## Features  
- **URL Scanning**: Leverages VirusTotal's URL Scan API to evaluate potential phishing threats.  
- **WHOIS Lookup**: Retrieves WHOIS information for the given URL domain.  
- **Sandbox Execution**: Automatically executes URLs in a VirtualBox virtual machine for further analysis.  
- **Logging**: Maintains a log file `DetectPhishingScanner.log` for error and usage tracking.

## Requirements  

### Python Modules  
Install the required modules using the following command:  
```bash
pip install requests python-dotenv
```

## Environment Variables
**Create a .env file with the following variables**:
```env
VIRUSTOTAL_API_KEY=<Your VirusTotal API Key>
VM_NAME=<Your VirtualBox VM Name>
VM_USERNAME=<Your VM Username>
VM_PASSWORD=<Your VM Password>
```

## Other Dependencies
- **VirtualBox**: Ensure VirtualBox is installed and the VM is configured correctly for automated login and analysis.
- **Firefox**: The browser must be installed in the VM for dynamic URL analysis.
- **VBoxManage**: VirtualBox must accept command-line VBoxManage commands.
- **Terminal AutoStart Upon Login**: This can be done by clicking application (on top left) > searching Sessions and Startup > Application AutoStart > add > Name: Terminal, Command: xfce4-terminal > OK (to save changes)

## Usage
Run the script using the following command:
```bash
python DetectPhishing.py <URL> <output_file>
```

## Example
```bash
python DetectPhishing.py http://malicious.example.com phishing_report.json
```

## Workflow
1. **Input**: The script accepts a URL and an output filename as arguments.
2. **URL Scanning**: The URL is submitted to VirusTotal for a scan.
3. **WHOIS Lookup**: Retrieves WHOIS data for the domain.
4. **Logging**: Saves results in the output file and logs events/errors in DetectPhishingScanner.log.
5. **VirtualBox Execution**: Starts the VirtualBox VM, automates login, and opens the URL for dynamic analysis.

## Output
- **Output File**:
Contains the VirusTotal scan results and WHOIS data in JSON format.
- **Log File**:
Logs activity and errors in DetectPhishingScanner.log.

## Example Log Output
```plaintext
2024-12-15 10:00:00 - INFO - Submitting URL http://malicious.example.com for scanning on VirusTotal...
2024-12-15 10:00:30 - INFO - Scan submitted successfully. Scan ID: abc123xyz
2024-12-15 10:01:10 - INFO - Fetching scan report for Scan ID: abc123xyz...
2024-12-15 10:01:20 - INFO - The URL has been flagged by 10 out of 96 scanners.
2024-12-15 10:01:40 - INFO - Fetching WHOIS information for domain: malicious.example.com...
2024-12-15 10:01:50 - INFO - WHOIS information saved to phishing_report.json
```

## Notes
**Ensure the .env file is properly configured for seamless execution.
Adjust VM boot times and VirtualBox configurations as necessary to match your environment.**


