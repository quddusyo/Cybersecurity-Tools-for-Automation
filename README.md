# Welcome to my Cybersecurity Tools for Automation Repo!
Author: Yousuf Quddus
Automated Scripts for Common Cybersecurity Practices
---

## Repositories
- 📜 Attacks, LinuxScripts, MalwareAnalysisScript, Monitoring&Backup, Scapy, WindowsScripts
- 🔒 PhishingLinkDetector
- 🎣 KillPhish

---

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Introduction](#disclaimer)

---

## Introduction
A collection of my custom cybersecurity tools, scripts, and projects in (mostly) python.
Some repositories include a README within the project scope while others include usage information 
in the beginning of the script.

---

## Features
Script:PhishingLinkDetector
Features:
- **URL Scanning**: Leverages VirusTotal's URL Scan API to evaluate potential phishing threats.
- **WHOIS Lookup**: Retrieves WHOIS information for the given URL domain.
- **Sandbox Execution**: Automatically executes URLs in a VirtualBox virtual machine for further analysis.
- **Logging**: Maintains a log file `DetectPhishingScanner.log` for error and usage tracking.

Script: KillPhish
Features:
- **Register / Login page**: Used OAuth for seamless login and registration.
- **User Dashboard**: Beautiful UI for a professional experience. 
- **Phishing Email Simulator**: Write up an email template and send to employees in the company, allows sender to spoof email address of choice for a more realistic experience.
- **Phishing Gamified Training Simulator**: Prompts users emails and the user clicks 'malicious' or 'safe' alongside a detailed explanation.
- **Email Link Click Notification**: Record users who clicked the link.

---

## Installation
Steps to install and set up your project locally:

1. Clone the Repository:
   ```bash
   git clone https://github.com/quddusyo/Cybersecurity-Tools-for-Automation.git

2. Download Dependancies:
   ```bash
   npm install

3. To Run App:
   Check specific script for useage details on README or within the code comments.

---

## Disclaimer
These scripts are provided for educational and research purposes only. They were designed to demonstrate cybersecurity automation techniques and is not intended for use in any unauthorized, illegal, or unethical activities. The author does not condone or support any malicious use of this script or any related tools.

By using this script, you acknowledge that it is your responsibility to ensure that its use complies with all applicable laws and regulations. The author(s) assume no liability for any damage or consequences resulting from the use of this script.

Use this script in a controlled, ethical, and legal environment only, such as in authorized penetration testing, educational labs, or security research environments. Always obtain proper authorization before testing or scanning any systems or networks.
