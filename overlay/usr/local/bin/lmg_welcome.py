#!/usr/bin/env python3
import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK = "#0b0f19"
CARD_BG = "#161e2e"
TEXT_COLOR = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#38bdf8"
ACCENT_NEON = "#00f0ff"
BUTTON_BG = "#1e293b"
BUTTON_HOVER = "#334155"

class LMGWelcomeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG OS Welcome")
        self.geometry("780x560")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header_frame = tk.Frame(self, bg=CARD_BG, pady=15, padx=20)
        header_frame.pack(fill="x", padx=15, pady=15)

        title_label = tk.Label(
            header_frame,
            text="Welcome to LMG OS 1.0.0",
            font=("Helvetica", 20, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        )
        title_label.pack(anchor="w")

        subtitle_label = tk.Label(
            header_frame,
            text="Logic Mind Grid OS — Powered by MineswordTeam | Debian 13.6 (Trixie) amd64",
            font=("Helvetica", 10),
            fg=TEXT_MUTED,
            bg=CARD_BG
        )
        subtitle_label.pack(anchor="w", pady=(2, 0))

        # Main Layout
        main_frame = tk.Frame(self, bg=BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Left Column - Quick Info
        left_col = tk.Frame(main_frame, bg=CARD_BG, padx=15, pady=15, width=280)
        left_col.pack(side="left", fill="both", expand=False, padx=(0, 10))

        tk.Label(
            left_col,
            text="System Overview",
            font=("Helvetica", 13, "bold"),
            fg=ACCENT_BLUE,
            bg=CARD_BG
        ).pack(anchor="w", pady=(0, 10))

        sys_info = self.get_sys_summary()
        for key, val in sys_info.items():
            k_lbl = tk.Label(left_col, text=f"{key}:", font=("Helvetica", 9, "bold"), fg=TEXT_MUTED, bg=CARD_BG)
            k_lbl.pack(anchor="w", pady=(4, 0))
            v_lbl = tk.Label(left_col, text=val, font=("Helvetica", 10), fg=TEXT_COLOR, bg=CARD_BG, justify="left", wraplength=250)
            v_lbl.pack(anchor="w")

        # Right Column - App Launchers
        right_col = tk.Frame(main_frame, bg=BG_DARK)
        right_col.pack(side="right", fill="both", expand=True)

        tk.Label(
            right_col,
            text="LMG Utilities & System Shortcuts",
            font=("Helvetica", 13, "bold"),
            fg=TEXT_COLOR,
            bg=BG_DARK
        ).pack(anchor="w", pady=(0, 10))

        grid_frame = tk.Frame(right_col, bg=BG_DARK)
        grid_frame.pack(fill="both", expand=True)

        apps = [
            ("LMG System", "System Info & Details", "lmg-system"),
            ("LMG RAM", "RAM Monitor & Optimizer", "lmg-ram"),
            ("LMG Test", "Hardware Diagnostics", "lmg-test"),
            ("LMG Hardware", "Detailed Specs", "lmg-hardware"),
            ("LMG Disk", "Storage & Drives", "lmg-disk"),
            ("LMG Cleaner", "System Maintenance", "lmg-cleaner"),
            ("LMG Update", "Package Updater", "lmg-update"),
            ("LMG Driver", "Driver Assistant", "lmg-driver"),
            ("LMG Gaming", "Gaming Tweaks", "lmg-gaming"),
            ("LMG Startup", "Autostart Manager", "lmg-startup"),
            ("Install LMG OS", "OS Installer", "calamares"),
            ("XFCE Settings", "Desktop Settings", "xfce4-settings-manager"),
        ]

        row, col = 0, 0
        for name, desc, cmd in apps:
            btn_card = tk.Frame(grid_frame, bg=CARD_BG, padx=10, pady=8, highlightbackground=BUTTON_BG, highlightthickness=1)
            btn_card.grid(row=row, column=col, sticky="nsew", padx=4, pady=4)
            grid_frame.columnconfigure(col, weight=1)
            grid_frame.rowconfigure(row, weight=1)

            btn_title = tk.Label(btn_card, text=name, font=("Helvetica", 10, "bold"), fg=ACCENT_BLUE, bg=CARD_BG, cursor="hand2")
            btn_title.pack(anchor="w")

            btn_desc = tk.Label(btn_card, text=desc, font=("Helvetica", 8), fg=TEXT_MUTED, bg=CARD_BG, cursor="hand2")
            btn_desc.pack(anchor="w")

            for widget in (btn_card, btn_title, btn_desc):
                widget.bind("<Button-1>", lambda e, c=cmd: self.launch_app(c))

            col += 1
            if col > 2:
                col = 0
                row += 1

    def get_sys_summary(self):
        kernel = subprocess.getoutput("uname -r")
        arch = subprocess.getoutput("uname -m")
        mem = subprocess.getoutput("free -h | awk '/Mem:/ {print $3 \" / \" $2}'")
        host = subprocess.getoutput("hostname")
        return {
            "OS": "LMG OS 1.0.0",
            "Base": "Debian 13.6 (Trixie)",
            "Kernel": kernel,
            "Architecture": arch,
            "Memory Usage": mem,
            "Hostname": host
        }

    def launch_app(self, cmd):
        try:
            subprocess.Popen(cmd.split())
        except Exception as e:
            messagebox.showerror("Launch Error", f"Unable to launch '{cmd}': {str(e)}")

if __name__ == "__main__":
    app = LMGWelcomeApp()
    app.mainloop()
