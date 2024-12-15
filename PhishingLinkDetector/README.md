# DetectPhishing.py

## Author  
**Yousuf A. Quddus**

## Description  
`DetectPhishing.py` is a Python script designed to analyze URLs for phishing activity. It integrates with the **VirusTotal API** to perform URL scans, fetch WHOIS information, and log the results. Additionally, it utilizes **VirtualBox** for sandboxed URL execution, allowing for dynamic analysis using user-specified tools. Logs are generated to ensure transparency and traceability.

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

##Environment Variables
**Create a .env file with the following variables**:
