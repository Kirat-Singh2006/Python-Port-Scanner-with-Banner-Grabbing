import socket
import re

# Regex patterns for validating input
ip_add_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
port_range_pattern = re.compile("([0-9]+)-([0-9]+)")

port_min = 0
port_max = 65535
open_ports = []

# Banner
from datetime import datetime
from colorama import init, Fore, Style

init()

banner = (
    "\033[38;5;205m"  # Start bright pink
    r"""
  _____                _____        ______  _____   ______         _____    ____   ____ 
 |\    \   _____   ___|\    \   ___|\     \|\    \ |\     \    ___|\    \  |    | |    |
 | |    | /    /| |    |\    \ |     \     \\\    \| \     \  /    /\    \ |    | |    |
 \/     / |    || |    | |    ||     ,_____/|\|    \  \     ||    |  |    ||    |_|    |
 /     /_  \   \/ |    |/____/ |     \--'\_|/ |     \  |    ||    |  |____||    .-.    |
|     // \  \   \ |    |\    \ |     /___/|   |      \ |    ||    |   ____ |    | |    |
|    |/   \ |    ||    | |    ||     \____|\  |    |\ \|    ||    |  |    ||    | |    |
|\ ___/\   \|   /||____| |____||____ '     /| |____||\_____/||\ ___\/    /||____| |____|
| |   | \______/ ||    | |    ||    /_____/ | |    |/ \|   ||| |   /____/ ||    | |    |
 \|___|/\ |    | ||____| |____||____|     | / |____|   |___|/ \|___|    | /|____| |____|
    \(   \|____|/   \(     )/    \( |_____|/    \(       )/     \( |____|/   \(     )/  
     '      )/       '     '      '    )/        '       '       '   )/       '     '
"""
    "\033[0m"  # Reset color
)

print(banner)

print(Fore.WHITE + "\n****************************************************************")
print("*  Copyright of wrench project, 2025                           *")
print(f"*  Loaded at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                *")
print("****************************************************************" + Style.RESET_ALL)

# Get target IP
while True:
    ip_add_entered = input("Please enter the IP address you want to scan: ").strip()
    if ip_add_pattern.search(ip_add_entered):
        print(f"{ip_add_entered} is a valid IP address.")
        break
    else:
        print("Invalid IP address format. Try again.")

# Get port range
while True:
    print("Please enter the range of ports you want to scan in the format: <int>-<int> (e.g., 20-80)")
    port_range = input("Enter port range: ")
    port_range_validity = port_range_pattern.search(port_range.replace(" ", ""))
    if port_range_validity:
        port_min = int(port_range_validity.group(1))
        port_max = int(port_range_validity.group(2))
        break
    else:
        print("Invalid port range format. Try again.")

# Scan ports
for port in range(port_min, port_max + 1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            s.connect((ip_add_entered, port))
            # Simple heuristic: if HTTP port, send GET request; else just receive banner
            if port in [80, 8080, 8000, 443]:
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()
            else:
                banner = s.recv(1024).decode(errors="ignore").strip()

            open_ports.append(port)
            print(f"[OPEN] Port {port} is open")

            # Banner grabbing
            try:
                # Send an HTTP request to provoke banner
                s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                banner = s.recv(1024).decode(errors="ignore").strip()
                if banner:
                    print(f"[BANNER] {banner}")
                else:
                    print("[BANNER] No banner received.")

            except Exception as e:
                print(f"[BANNER] Could not grab banner: {e}")

    except:
        print(f"[CLOSED] Port {port} closed or filtered")

# Summary
print("\nScan complete.")
if open_ports:
    print("Open ports found:")
    for port in open_ports:
        print(f"  - Port {port}")
else:
    print("No open ports found.")
