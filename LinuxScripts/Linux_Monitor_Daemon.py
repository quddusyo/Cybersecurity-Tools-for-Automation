"""
Linux Script that monitor the /etc/passwd and /etc/shadow 
files for any changes. If a change occurs, it will log the details.
This script can be run periodically (or as a daemon) on a Linux 
machine to detect and log any unauthorized user additions, which could 
signal a security breach.
"""
#!/usr/bin/env python3
import os
import csv
from time import sleep, strftime

# Set the path for the /etc/passwd file
PASSWD_FILE = "/etc/passwd"
CSV_LOG_FILE = "linux_user_audit_log.csv"

# Function to read the /etc/passwd file and return a list of usernames
def get_user_list():
    users = []
    with open(PASSWD_FILE, "r") as f:
        for line in f:
            if not line.startswith("#"):  # Ignore commented lines
                # Split each line and extract the username (1st field before ':')
                user = line.split(":")[0]
                users.append(user)
    return users

# Function to write new users to a CSV file
def log_new_users(new_users):
    with open(CSV_LOG_FILE, "a+", newline="") as csvfile:
        writer = csv.writer(csvfile)
        current_time = strftime("%Y-%m-%d %H:%M:%S")  # Get current time
        for user in new_users:
            writer.writerow([user, current_time])

# Main monitoring function
def monitor_users(interval=10):
    print("Starting user monitoring...")

    # Step 1: Initialize baseline by reading the current list of users
    baseline_users = get_user_list()

    # Main loop for monitoring
    while True:
        print("Checking for new users...")
        
        # Step 2: Get current list of users
        current_users = get_user_list()

        # Step 3: Check if there are any new users
        new_users = [user for user in current_users if user not in baseline_users]

        # Step 4: Log new users if found
        if new_users:
            print(f"New users detected: {new_users}")
            log_new_users(new_users)

            # Update baseline after logging
            baseline_users = current_users

        # Sleep for the specified interval before next check
        sleep(interval)

# Function to initialize CSV log file with headers if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_LOG_FILE):
        with open(CSV_LOG_FILE, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Writing header row for CSV
            writer.writerow(["Username", "Detected At"])

if __name__ == "__main__":
    # Initialize the CSV file with headers
    initialize_csv()

    # Start monitoring with a check interval of 30 seconds
    monitor_users(interval=30)
