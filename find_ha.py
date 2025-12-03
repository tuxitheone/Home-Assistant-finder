#!/usr/bin/env python3
import ipaddress
import socket
import time
import sys

PORT = 8123
SLEEP_SECONDS = 5
CIDR_PREFIX = 24  # Antag /24-netværk (fx 192.168.2.0/24)

def get_local_ipv4():
    '''
    Find lokal IPv4-adresse på tværs af Windows og Linux.
    Vi laver et "falsk" UDP-kald til 8.8.8.8 for at finde den udgående IP.
    Der sendes ingen rigtig trafik, men OS vælger det rigtige interface.
    '''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
    except OSError:
        # Fallback – virker ofte, men kan give 127.x på nogle Linux-installationer
        ip = socket.gethostbyname(socket.gethostname())

    if ip.startswith("127."):
        print("[FEJL] Kunne ikke finde en ikke-127.x IPv4-adresse.")
        print("       Er du forbundet til et netværk?")
        sys.exit(1)

    return ip

def get_network():
    ip = get_local_ipv4()
    try:
        net = ipaddress.ip_network(f"{ip}/{CIDR_PREFIX}", strict=False)
    except ValueError as e:
        print(f"[FEJL] Ugyldigt netværk for IP {ip}: {e}")
        sys.exit(1)
    return net

def scan_port(host, port=PORT, timeout=0.3):
    try:
        with socket.create_connection((str(host), port), timeout=timeout):
            return True
    except OSError:
        return False

def main():
    print("🔍 Home Assistant Auto-Finder (Windows + Linux)")
    print(f"   Scanner efter Home Assistant på port {PORT}")
    print("   Kører indtil en server findes – stop med CTRL+C\n")

    net = get_network()
    print(f"🌐 Opdaget lokal IP-range (baseret på /{CIDR_PREFIX}): {net}\n")

    try:
        while True:
            found = False
            for host in net.hosts():
                if scan_port(host):
                    print(f"✅ Fundet Home Assistant: http://{host}:{PORT}")
                    found = True
                    break

            if found:
                print("\nFærdig. Åbn adressen ovenfor i din browser.")
                return

            print(f"⏳ Ingen Home Assistant fundet endnu... prøver igen om {SLEEP_SECONDS} sekunder.")
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        print("\n🛑 Afbrudt af bruger (CTRL+C). Farvel!")

if __name__ == '__main__':
    main()
