#!/usr/bin/env python3
import sys
import os
import subprocess
import glob
import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK = "#0b0f19"
CARD_BG = "#161e2e"
TEXT_COLOR = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#38bdf8"
ACCENT_NEON = "#00f0ff"
BORDER_COLOR = "#1e293b"

class LMGStartupApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Startup — Startup Applications & Services Manager")
        self.geometry("720x520")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG Startup & Service Manager",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Inspect desktop autostart applications and system background services",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Tabs
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Desktop Autostart Tab
        auto_frame = tk.Frame(notebook, bg=CARD_BG, padx=10, pady=10)
        notebook.add(auto_frame, text="Desktop Autostart Apps")

        columns_auto = ("name", "cmd", "location")
        self.tree_auto = ttk.Treeview(auto_frame, columns=columns_auto, show="headings")
        self.tree_auto.heading("name", text="Application Name")
        self.tree_auto.heading("cmd", text="Exec Command")
        self.tree_auto.heading("location", text="Desktop File Path")

        self.tree_auto.column("name", width=180, anchor="w")
        self.tree_auto.column("cmd", width=220, anchor="w")
        self.tree_auto.column("location", width=260, anchor="w")

        self.tree_auto.pack(fill="both", expand=True)

        # System Services Tab
        svc_frame = tk.Frame(notebook, bg=CARD_BG, padx=10, pady=10)
        notebook.add(svc_frame, text="Systemd Active Services")

        columns_svc = ("unit", "load", "active", "sub", "desc")
        self.tree_svc = ttk.Treeview(svc_frame, columns=columns_svc, show="headings")
        self.tree_svc.heading("unit", text="Service Unit")
        self.tree_svc.heading("load", text="Load State")
        self.tree_svc.heading("active", text="Active State")
        self.tree_svc.heading("sub", text="Sub State")
        self.tree_svc.heading("desc", text="Description")

        self.tree_svc.column("unit", width=180, anchor="w")
        self.tree_svc.column("load", width=80, anchor="center")
        self.tree_svc.column("active", width=80, anchor="center")
        self.tree_svc.column("sub", width=80, anchor="center")
        self.tree_svc.column("desc", width=240, anchor="w")

        self.tree_svc.pack(fill="both", expand=True)

        self.load_autostart()
        self.load_services()

    def load_autostart(self):
        autostart_dirs = [
            os.path.expanduser("~/.config/autostart"),
            "/etc/xdg/autostart"
        ]
        for d in autostart_dirs:
            if os.path.exists(d):
                for filepath in glob.glob(os.path.join(d, "*.desktop")):
                    name = os.path.basename(filepath)
                    cmd = "N/A"
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            for line in f:
                                if line.startswith("Name=") and name == os.path.basename(filepath):
                                    name = line.split("=", 1)[1].strip()
                                elif line.startswith("Exec="):
                                    cmd = line.split("=", 1)[1].strip()
                    except Exception:
                        pass
                    self.tree_auto.insert("", "end", values=(name, cmd, filepath))

    def load_services(self):
        res = subprocess.getoutput("systemctl list-units --type=service --state=running --no-legend 2>/dev/null")
        for line in res.strip().split("\n"):
            if line:
                parts = line.split(maxsplit=4)
                if len(parts) == 5:
                    self.tree_svc.insert("", "end", values=parts)

if __name__ == "__main__":
    app = LMGStartupApp()
    app.mainloop()
