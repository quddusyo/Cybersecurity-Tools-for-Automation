'''
Python script which utilizes ctypes library to disable critical executabled by renaming files. 
Included return to default seting option aswell.
'''

import os
import ctypes

def rename_executable(target_path, new_name):
    """
    Renames a file to disable its functionality.
    """
    if os.path.exists(target_path):
        try:
            # Construct new path
            new_path = os.path.join(os.path.dirname(target_path), new_name)
            os.rename(target_path, new_path)
            print(f"[+] Renamed {target_path} to {new_path}")
        except PermissionError:
            print(f"[-] Permission denied: Could not rename {target_path}")
        except Exception as e:
            print(f"[-] Error renaming {target_path}: {e}")
    else:
        print(f"[-] File not found: {target_path}")

def restore_executable(target_path, original_name):
    """
    Restores a previously renamed executable.
    """
    if os.path.exists(target_path):
        try:
            original_path = os.path.join(os.path.dirname(target_path), original_name)
            os.rename(target_path, original_path)
            print(f"[+] Restored {target_path} to {original_path}")
        except PermissionError:
            print(f"[-] Permission denied: Could not restore {target_path}")
        except Exception as e:
            print(f"[-] Error restoring {target_path}: {e}")
    else:
        print(f"[-] File not found: {target_path}")

def disable_critical_executables():
    """
    Disables critical executables by renaming them.
    can add desired executable paths to disable.
    """
    critical_files = [
        r"C:\Windows\System32\taskmgr.exe",  # Task Manager
        r"C:\Windows\explorer.exe",          # Explorer
        r"C:\Windows\System32\cmd.exe",      # Command Prompt
    ]

    for file in critical_files:
        rename_executable(file, os.path.basename(file) + ".disabled")

def enable_critical_executables():
    """
    Restores critical executables by renaming them back to their original names.
    """
    critical_files = [
        (r"C:\Windows\System32\taskmgr.exe.disabled", "taskmgr.exe"),
        (r"C:\Windows\explorer.exe.disabled", "explorer.exe"),
        (r"C:\Windows\System32\cmd.exe.disabled", "cmd.exe"),
    ]

    for file, original_name in critical_files:
        restore_executable(file, original_name)

if __name__ == "__main__":
    print("Choose an option:")
    print("1. Disable critical executables")
    print("2. Enable critical executables")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        disable_critical_executables()
    elif choice == "2":
        enable_critical_executables()
    else:
        print("[-] Invalid choice.")
