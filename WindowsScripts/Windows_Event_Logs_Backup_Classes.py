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

# Define a class for File Monitoring
class FileMonitor:
    def __init__(self, file_paths):
        self.file_paths = file_paths  # List of important files
        self.file_report = []  # Stores the report data
    
    # Method to check each file for existence, size, creation, and modification times
    def check_files(self):
        for file_path in self.file_paths:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)  # Get file size

                # Get creation and last modification times
                creation_time = os.path.getctime(file_path)
                creation_time_formatted = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

                modification_time = os.path.getmtime(file_path)
                modification_time_formatted = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')

                print(f"{file_path} exists with size {file_size} bytes, created on {creation_time_formatted}, last modified on {modification_time_formatted}.")
            else:
                file_size = 0
                creation_time_formatted = "N/A"
                modification_time_formatted = "N/A"
                print(f"{file_path} does not exist.")
            
            # Append the result to the report
            self.file_report.append([file_path, os.path.exists(file_path), file_size, creation_time_formatted, modification_time_formatted])
    
    # Method to write the report to a CSV file
    def write_report(self, csv_filename):
        with open(csv_filename, mode="a+", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["File Path", "Exists", "File Size (Bytes)", "Creation Date & Time", "Last Modified Date & Time"])

            # Write each file info into the CSV
            for file_info in self.file_report:
                writer.writerow(file_info)

        print(f"File report saved to {csv_filename}.")

# List of important files to monitor
important_files = [
    r"C:\Windows\System32\config\SYSTEM",
    r"C:\Windows\System32\config\SOFTWARE",
    r"C:\Windows\System32\drivers\etc\hosts",
    r"C:\Windows\System32\winevt\Logs\System.evtx",
    r"C:\Windows\System32\winevt\Logs\Application.evtx"
]

# Main script execution
if __name__ == "__main__":
    # Create an instance of the FileMonitor class
    file_monitor = FileMonitor(important_files)
    
    # Check the files
    file_monitor.check_files()
    
    # Write the report to CSV
    file_monitor.write_report("windows_file_report.csv")
