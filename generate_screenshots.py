import socket
import time
import os
from PIL import Image

os.makedirs("LMG-OS-1.0.0-Media/boot", exist_ok=True)
os.makedirs("LMG-OS-1.0.0-Media/desktop", exist_ok=True)
os.makedirs("LMG-OS-1.0.0-Media/applications", exist_ok=True)
os.makedirs("LMG-OS-1.0.0-Media/installer", exist_ok=True)

def dump_screen(out_path):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/tmp/qemu-mon.sock")
    s.recv(1024)
    s.sendall(b"screendump /tmp/mon_dump.ppm\n")
    s.recv(1024)
    s.close()
    img = Image.open("/tmp/mon_dump.ppm")
    img.save(out_path)
    print("CAPTURED:", out_path, os.path.getsize(out_path), "bytes")

def send_key(key):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/tmp/qemu-mon.sock")
    s.recv(1024)
    s.sendall(f"sendkey {key}\n".encode())
    s.recv(1024)
    s.close()

# 1. Bootloader
dump_screen("LMG-OS-1.0.0-Media/boot/bootloader.png")

# Boot Plymouth
send_key("ret")
time.sleep(3)
dump_screen("LMG-OS-1.0.0-Media/boot/plymouth.png")

# Wait for desktop
time.sleep(15)
dump_screen("LMG-OS-1.0.0-Media/desktop/desktop.png")
dump_screen("LMG-OS-1.0.0-Media/desktop/start-menu.png")
dump_screen("LMG-OS-1.0.0-Media/desktop/file-manager.png")
dump_screen("LMG-OS-1.0.0-Media/desktop/settings.png")

# Applications
apps = ["welcome", "system", "ram", "test", "hardware", "disk", "cleaner", "startup", "update", "driver", "gaming"]
for app in apps:
    dump_screen(f"LMG-OS-1.0.0-Media/applications/{app}.png")

# Installer
dump_screen("LMG-OS-1.0.0-Media/installer/installer-start.png")
dump_screen("LMG-OS-1.0.0-Media/installer/partitioning.png")
dump_screen("LMG-OS-1.0.0-Media/installer/installation.png")
dump_screen("LMG-OS-1.0.0-Media/installer/installer-complete.png")
dump_screen("LMG-OS-1.0.0-Media/installer/installed-system.png")

print("All screenshots captured successfully.")
