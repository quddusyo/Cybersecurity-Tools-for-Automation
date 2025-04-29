# Welcome to my Cybersecurity Tools for Automation Repo!
**Author: Yousuf Quddus**<br/>
<br/>
Automated Scripts for Common Cybersecurity Practices
---

## Repositories
- 📜 Attacks, LinuxScripts, MalwareAnalysisScript, Monitoring&Backup, Scapy, WindowsScripts
- 🔒 `PhishingLinkDetector`
- 🎣 `KillPhish`

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Disclaimer](#disclaimer)

---

## Introduction
A collection of my custom cybersecurity tools, scripts, and projects in (mostly) python.
Some repositories include a `README` within the project scope while others include usage information 
in the beginning of the script.

---

## Features
Script: `PhishingLinkDetector` Public Repo
Features:
- **URL Scanning**: Leverages VirusTotal's URL Scan API to evaluate potential phishing threats.
- **WHOIS Lookup**: Retrieves WHOIS information for the given URL domain.
- **Sandbox Execution**: Automatically executes URLs in a VirtualBox virtual machine for further analysis.
- **Logging**: Maintains a log file `DetectPhishingScanner.log` for error and usage tracking.<br/><br/>

Script: `KillPhish` Private Repo
Features:
- **User Dashboard**: Neat and tidy UI for a professional experience. 
- **AI Phishing Email Simulator**: Write up an email template and send to employees in the company, allows sender to spoof email address of choice for a more realistic experience with the use of AI.
- **Phishing Gamified Training**: Prompts users emails and the user clicks 'malicious' or 'safe' alongside a detailed explanation. There are real word examples of phishing emails alongside true and false questions and answers for a broader understanding categorized by their level of difficulty.
- **Cross Browser & Responsive**: This application is modified to allow all devices to access and complete the comtent on various browsers like edge, firefox, google, etc.
- **Certificate for Phishing Awareness & Training**: This application prints a certificate of completion (CPAT+) upon completion.

---

## Installation
Steps to install and set up environment to your project locally:

1. Clone the Repository:
   ```bash
   git clone https://github.com/quddusyo/Cybersecurity-Tools-for-Automation.git

2. Download Dependancies go to project folder and run:
   ```bash
   npm install

3. Run App:
   Check specific script for a detailed useage on the `README` section or within the code comments.

---

## Disclaimer
These scripts are provided for educational and research purposes only. They were designed to demonstrate cybersecurity automation techniques and is not intended for use in any unauthorized, illegal, or unethical activities. The author does not condone or support any malicious use of this script or any related tools.

By using this script, you acknowledge that it is your responsibility to ensure that its use complies with all applicable laws and regulations. The author(s) assume no liability for any damage or consequences resulting from the use of this script.

Use this script in a controlled, ethical, and legal environment only, such as in authorized penetration testing, educational labs, or security research environments. Always obtain proper authorization before testing or scanning any systems or networks.
