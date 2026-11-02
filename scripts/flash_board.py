"""
Interactive ESP32 & NodeMCU (ESP8266) Flasher Utility
Auto-detects COM ports and flashes precompiled binaries for:
- ESP32 Receiver (RX)
- ESP32 Transmitter (TX)
- NodeMCU ESP8266 Transmitter (TX)

Includes automatic port release (kills zombie serial monitors)
and modern esptool v5 argument syntax.
"""

import sys
import os
import subprocess
import serial.tools.list_ports

def release_serial_locks():
    """Terminate background serial monitors (like Arduino IDE serial-monitor) that hold COM locks."""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "serial-monitor.exe"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def get_ports():
    ports = serial.tools.list_ports.comports()
    return [p.device for p in ports]

def flash(target, port):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = target.lower()

    # Free any active serial locks before attempting flash
    release_serial_locks()

    if target in ["nodemcu", "nodemcu_tx", "esp8266"]:
        # Flash ESP8266 NodeMCU
        bin_dir = os.path.join(base_dir, "bin", "nodemcu_tx")
        firmware = os.path.join(bin_dir, "firmware.bin")
        if not os.path.exists(firmware):
            print(f"[ERROR] NodeMCU firmware not found at {firmware}")
            return False

        cmd = [
            sys.executable, "-m", "esptool",
            "--chip", "esp8266",
            "--port", port,
            "--baud", "460800",
            "--before", "default-reset",
            "--after", "hard-reset",
            "write-flash",
            "0x0", firmware
        ]
        chip_label = "NodeMCU (ESP8266) TX"
    else:
        # Flash ESP32 (TX or RX)
        bin_dir = os.path.join(base_dir, "bin", target)
        bootloader = os.path.join(bin_dir, "bootloader.bin")
        partitions = os.path.join(bin_dir, "partitions.bin")
        firmware = os.path.join(bin_dir, "firmware.bin")
        
        if not (os.path.exists(bootloader) and os.path.exists(partitions) and os.path.exists(firmware)):
            print(f"[ERROR] Binary files for {target.upper()} not found in {bin_dir}")
            return False

        cmd = [
            sys.executable, "-m", "esptool",
            "--chip", "esp32",
            "--port", port,
            "--baud", "460800",
            "--before", "default-reset",
            "--after", "hard-reset",
            "write-flash", "-z",
            "--flash-mode", "dio",
            "--flash-freq", "40m",
            "--flash-size", "detect",
            "0x1000", bootloader,
            "0x8000", partitions,
            "0x10000", firmware
        ]
        chip_label = f"ESP32 {target.upper()}"
    
    print(f"\n=================================================")
    print(f"  Flashing {chip_label} to {port}...")
    print(f"=================================================\n")
    print("Command:", " ".join(cmd))
    
    try:
        ret = subprocess.run(cmd)
        if ret.returncode == 0:
            print(f"\n[SUCCESS] {chip_label} flashed successfully onto {port}!\n")
            return True
        else:
            print(f"\n[FAILED] esptool exited with code {ret.returncode}.")
            print("\nTroubleshooting Tips:")
            print("1. If 'Access is denied': Close the Serial Monitor in Arduino IDE (it locks the port).")
            print("2. If 'Connecting...___...': Hold down the 'BOOT' / 'FLASH' button on the board for 2 seconds.")
            return False
    except Exception as e:
        print(f"[ERROR] Could not execute esptool: {e}")
        return False

if __name__ == "__main__":
    target = None
    port = None

    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
    if len(sys.argv) > 2:
        port = sys.argv[2]

    # Free background serial locks
    release_serial_locks()

    ports = get_ports()
    if not ports and not port:
        print("[WARNING] No active COM ports detected!")
        print("Please plug in your board via a data-capable USB cable and run again.")
        input("Press Enter to exit...")
        sys.exit(1)

    if not port:
        print("=================================================")
        print("   WiFi Vital Signs Radar - Firmware Flasher     ")
        print("=================================================")
        print("\nAvailable COM Ports:")
        for idx, p in enumerate(ports):
            print(f"  [{idx + 1}] {p}")
            
        choice = input(f"\nSelect COM Port number [1]: ").strip()
        port_idx = int(choice) - 1 if choice.isdigit() else 0
        if port_idx < 0 or port_idx >= len(ports):
            port_idx = 0
        port = ports[port_idx]

    if not target:
        print("\nSelect Target Board:")
        print("  [1] NodeMCU (ESP8266) - Transmitter (TX)")
        print("  [2] ESP32             - Receiver (RX) [Connected to PC]")
        print("  [3] ESP32             - Transmitter (TX)")
        
        node_choice = input("Enter choice [1, 2, or 3]: ").strip()
        if node_choice == "1":
            target = "nodemcu_tx"
        elif node_choice == "3":
            target = "tx"
        else:
            target = "rx"

    flash(target, port)
    input("\nPress Enter to finish...")
