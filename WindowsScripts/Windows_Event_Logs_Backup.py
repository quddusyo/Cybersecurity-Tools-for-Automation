"""
This windows script will back up the Windows Event Logs 
using the wevtutil command to a backup directory.
Cyber Security Justification: This script serves as a lightweight, automated tool 
for file integrity monitoring, offering an extra layer of defense in detecting 
tampering or deletion of critical Windows system files. It contributes to system 
security by helping to detect attacks early, maintain the integrity of vital files, 
and aid in incident response. You can also see when the file was created alongside 
ast modified for a integrity check. 
"""
import os
import csv
from datetime import datetime

# List of important files to monitor in Windows
important_files = [
    r"C:\Windows\System32\config\SYSTEM",
    r"C:\Windows\System32\config\SOFTWARE",
    r"C:\Windows\System32\drivers\etc\hosts",
    r"C:\Windows\System32\winevt\Logs\System.evtx",
    r"C:\Windows\System32\winevt\Logs\Application.evtx"
]

# Function to check file existence, size, creation time, and modification time
def check_file(file_path):
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)  # Get file size in bytes

        # Get creation time and last modification time
        creation_time = os.path.getctime(file_path)
        creation_time_formatted = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

        modification_time = os.path.getmtime(file_path)
        modification_time_formatted = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

        return (True, file_size, creation_time_formatted, modification_time_formatted)
    else:
        return (False, 0, "N/A", "N/A")

# Write data to a CSV file with creation and modification times
def write_report(file_report):
    with open("windows_file_report.csv", mode="a+", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File Path", "Exists", "File Size (Bytes)", "Creation Date & Time", "Last Modified Date & Time"])

        # Loops through each file in the file_report list
        for file_info in file_report:
            writer.writerow(file_info)

# Main function to check the status of important files and generate a report
def main():
    # Initialize a list to hold the report data
    file_report = []
    
    # Loop to check the status of each file
    for file_path in important_files:
        file_exists, file_size, creation_time, modification_time = check_file(file_path)
        
        # Flow control to handle files based on their existence
        if file_exists:
            print(f"{file_path} exists with size {file_size} bytes, created on {creation_time}, last modified on {modification_time}.")
        else:
            print(f"{file_path} does not exist.")
        
        # Append the result to the file_report list
        file_report.append([file_path, file_exists, file_size, creation_time, modification_time])
    
    # Write the report to a CSV file
    write_report(file_report)
    print("File report with creation and modification date and time has been generated.")

if __name__ == "__main__":
    main()