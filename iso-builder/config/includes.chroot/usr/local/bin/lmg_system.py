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

class LMGSystemApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG System — LMG OS Information")
        self.geometry("680x520")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Top Header Banner
        header = tk.Frame(self, bg=CARD_BG, pady=15, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG OS 1.0.0",
            font=("Helvetica", 22, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Logic Mind Grid Operating System | Developed by MineswordTeam",
            font=("Helvetica", 10),
            fg=ACCENT_BLUE,
            bg=CARD_BG
        ).pack(anchor="w", pady=(2, 0))

        # System Details Grid Container
        content = tk.Frame(self, bg=BG_DARK)
        content.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        sys_details = self.gather_system_details()

        row = 0
        col = 0
        for section_title, details in sys_details.items():
            card = tk.Frame(content, bg=CARD_BG, padx=15, pady=12, highlightbackground=BORDER_COLOR, highlightthickness=1)
            card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
            content.columnconfigure(col, weight=1)
            content.rowconfigure(row, weight=1)

            tk.Label(
                card,
                text=section_title,
                font=("Helvetica", 12, "bold"),
                fg=ACCENT_NEON,
                bg=CARD_BG
            ).pack(anchor="w", pady=(0, 8))

            for k, v in details.items():
                item_frame = tk.Frame(card, bg=CARD_BG)
                item_frame.pack(fill="x", pady=2)
                tk.Label(item_frame, text=f"{k}:", font=("Helvetica", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG, width=14, anchor="w").pack(side="left")
                tk.Label(item_frame, text=v, font=("Helvetica", 9), fg=TEXT_COLOR, bg=CARD_BG, anchor="w", justify="left").pack(side="left", fill="x", expand=True)

            col += 1
            if col > 1:
                col = 0
                row += 1

    def gather_system_details(self):
        # Read real system data
        cpu_model = self.get_cpu_model()
        ram_info = subprocess.getoutput("free -h | awk '/Mem:/ {print $2 \" Total (\" $3 \" Used, \" $4 \" Free)\"}'")
        swap_info = subprocess.getoutput("free -h | awk '/Swap:/ {print $2 \" Total (\" $3 \" Used)\"}'")
        disk_info = subprocess.getoutput("df -h / | awk 'NR==2 {print $2 \" Total (\" $3 \" Used, \" $4 \" Available)\"}'")
        uptime = subprocess.getoutput("uptime -p").replace("up ", "")

        return {
            "OS & Branding": {
                "Distribution": "LMG OS (Logic Mind Grid OS)",
                "Version": "1.0.0",
                "Base": "Debian GNU/Linux 13.6 (Trixie)",
                "Team": "MineswordTeam",
                "Desktop": "XFCE 4"
            },
            "System Architecture": {
                "Architecture": platform.machine(),
                "Kernel Version": platform.release(),
                "Hostname": platform.node(),
                "Uptime": uptime if uptime else "N/A"
            },
            "Hardware Summary": {
                "Processor": cpu_model,
                "Total Memory": ram_info,
                "Swap Space": swap_info,
                "Root Disk Space": disk_info
            },
            "Environment": {
                "Python Version": platform.python_version(),
                "Init System": "systemd",
                "Package Format": "dpkg / apt",
                "Session Type": os.environ.get("XDG_SESSION_TYPE", "x11")
            }
        }

    def get_cpu_model(self):
        try:
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        except Exception:
            pass
        return platform.processor() or "x86_64 Processor"

if __name__ == "__main__":
    app = LMGSystemApp()
    app.mainloop()
