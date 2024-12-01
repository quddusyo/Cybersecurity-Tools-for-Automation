'''
Linux Script using classes that monitor the /etc/passwd and /etc/shadow 
files for any changes. If a change occurs, it will log the details.
This script can be run periodically (or as a daemon) on a Linux 
machine to detect and log any unauthorized user additions, which could 
signal a security breach.
'''
import os
import csv
from time import sleep, strftime


class UserMonitor:
    def __init__(self, passwd_file="/etc/passwd", csv_log_file="user_audit_log.csv", interval=30):
        self.passwd_file = passwd_file
        self.csv_log_file = csv_log_file
        self.interval = interval
        self.baseline_users = self.get_user_list()

    def get_user_list(self):
        """Read the /etc/passwd file and return a list of usernames."""
        users = []
        with open(self.passwd_file, "r") as f:
            for line in f:
                if not line.startswith("#"):  # Ignore commented lines
                    user = line.split(":")[0]
                    users.append(user)
        return users

    def log_new_users(self, new_users):
        """Log new users to a CSV file with the current timestamp."""
        with open(self.csv_log_file, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            current_time = strftime("%Y-%m-%d %H:%M:%S")  # Get current time
            for user in new_users:
                writer.writerow([user, current_time])

    def monitor_users(self):
        """Monitor users and log any new additions."""
        print("Starting user monitoring...")
        while True:
            print("Checking for new users...")
            current_users = self.get_user_list()

            # Check for new users
            new_users = [user for user in current_users if user not in self.baseline_users]

            # Log new users if found
            if new_users:
                print(f"New users detected: {new_users}")
                self.log_new_users(new_users)

                # Update baseline after logging
                self.baseline_users = current_users

            # Sleep for the specified interval before next check
            sleep(self.interval)


class CSVLogger:
    def __init__(self, csv_log_file="user_audit_log.csv"):
        self.csv_log_file = csv_log_file
        self.initialize_csv()

    def initialize_csv(self):
        """Initialize the CSV log file with headers if it doesn't exist."""
        if not os.path.exists(self.csv_log_file):
            with open(self.csv_log_file, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                # Writing header row for CSV
                writer.writerow(["Username", "Detected At"])


if __name__ == "__main__":
    # Initialize the CSV logger
    logger = CSVLogger()

    # Start the user monitor
    user_monitor = UserMonitor(csv_log_file=logger.csv_log_file)
    user_monitor.monitor_users()
