import subprocess
import re

def load_known_devices(filename="known_devices.txt"):
    try:
        with open(filename, "r") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        return []

known_devices = load_known_devices()

def add_to_known(mac, filename="known_devices.txt"):
    with open(filename, "a") as f:
        f.write(mac.lower() + "\n")
    print(f"✅ Added {mac} to known devices!")

def get_connected_devices():
    output = subprocess.check_output("arp -a", shell=True).decode()
    devices = []

    pattern = r"\? \(([\d.]+)\) at ([0-9a-f:]+)"
    for match in re.finditer(pattern, output, re.IGNORECASE):
        ip = match.group(1)
        mac = match.group(2).lower()

        if mac == "ff:ff:ff:ff:ff:ff" or ip.startswith("224."):
            continue

        devices.append((ip, mac))

    return devices

def check_for_unknowns():
    devices = get_connected_devices()
    for ip, mac in devices:
        if mac not in known_devices:
            print(f"⚠️ UNKNOWN DEVICE: IP = {ip}, MAC = {mac}")
        else:
            print(f"✅ Known device: IP = {ip}, MAC = {mac}")

check_for_unknowns()
