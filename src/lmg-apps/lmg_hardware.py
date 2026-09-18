#!/usr/bin/env python3
import sys
import os
import subprocess
import platform
import tkinter as tk
from tkinter import ttk

BG_DARK = "#0b0f19"
CARD_BG = "#161e2e"
TEXT_COLOR = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#38bdf8"
ACCENT_NEON = "#00f0ff"
BORDER_COLOR = "#1e293b"

class LMGHardwareApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Hardware — Hardware Inspector")
        self.geometry("740x580")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG Hardware Inspector",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Detailed hardware detection and component inventory",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Tabbed interface for hardware categories
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.add_hardware_tab(notebook, "Processor (CPU)", self.get_cpu_details())
        self.add_hardware_tab(notebook, "Graphics (GPU)", self.get_gpu_details())
        self.add_hardware_tab(notebook, "Memory (RAM)", self.get_ram_details())
        self.add_hardware_tab(notebook, "Storage Devices", self.get_storage_details())
        self.add_hardware_tab(notebook, "Network Adapters", self.get_network_details())
        self.add_hardware_tab(notebook, "Audio Devices", self.get_audio_details())

    def add_hardware_tab(self, notebook, title, details):
        frame = tk.Frame(notebook, bg=CARD_BG, padx=15, pady=15)
        notebook.add(frame, text=title)

        text_area = tk.Text(
            frame,
            bg=BG_DARK,
            fg=TEXT_COLOR,
            font=("Monospace", 9),
            bd=0,
            padx=10,
            pady=10,
            wrap="word"
        )
        text_area.pack(fill="both", expand=True)
        text_area.insert("1.0", details)
        text_area.config(state="disabled")

    def get_cpu_details(self):
        try:
            info = subprocess.getoutput("lscpu 2>/dev/null")
            if info and "Architecture" in info:
                return info
            with open("/proc/cpuinfo", "r") as f:
                return f.read()
        except Exception as e:
            return f"Error detecting CPU: {str(e)}"

    def get_gpu_details(self):
        res = subprocess.getoutput("lspci | grep -iE 'vga|3d|display' 2>/dev/null")
        if res:
            return res
        return "Standard VGA/Display Adapter (QEMU/KVM Virtual Graphics Adapter)"

    def get_ram_details(self):
        res = subprocess.getoutput("free -h; echo '\nMemory Layout:\n'; cat /proc/meminfo 2>/dev/null | head -n 15")
        return res if res else "RAM details unavailable"

    def get_storage_details(self):
        res = subprocess.getoutput("lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT 2>/dev/null")
        if res:
            return res
        return subprocess.getoutput("df -h")

    def get_network_details(self):
        res = subprocess.getoutput("ip addr 2>/dev/null")
        if res:
            return res
        return subprocess.getoutput("ifconfig 2>/dev/null") or "Network devices unavailable"

    def get_audio_details(self):
        res = subprocess.getoutput("lspci | grep -i audio 2>/dev/null")
        if res:
            return res
        return "Audio hardware details unavailable / Standard AC97/HDA Audio"

if __name__ == "__main__":
    app = LMGHardwareApp()
    app.mainloop()
