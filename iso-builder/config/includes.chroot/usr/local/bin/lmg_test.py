#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
import socket
import tkinter as tk
from tkinter import ttk

BG_DARK = "#0b0f19"
CARD_BG = "#161e2e"
TEXT_COLOR = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#38bdf8"
ACCENT_NEON = "#00f0ff"
COLOR_PASS = "#22c55e"
COLOR_FAIL = "#ef4444"
BORDER_COLOR = "#1e293b"
BUTTON_BG = "#1e293b"

class LMGTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Test — Diagnostic & System Verification")
        self.geometry("740x560")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG System Diagnostic Suite",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Real hardware verification and system health diagnostic tests",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Controls & Action
        top_bar = tk.Frame(self, bg=BG_DARK)
        top_bar.pack(fill="x", padx=15, pady=(0, 10))

        self.status_lbl = tk.Label(top_bar, text="Ready to execute diagnostics.", font=("Helvetica", 10, "bold"), fg=TEXT_COLOR, bg=BG_DARK)
        self.status_lbl.pack(side="left")

        btn_run = tk.Button(
            top_bar,
            text="Run System Diagnostic",
            font=("Helvetica", 10, "bold"),
            fg=ACCENT_NEON,
            bg=BUTTON_BG,
            activebackground=CARD_BG,
            activeforeground=ACCENT_NEON,
            bd=0,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.run_diagnostics
        )
        btn_run.pack(side="right")

        # Results Table
        card_frame = tk.Frame(self, bg=CARD_BG, padx=15, pady=15, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("category", "component", "status", "details")
        self.tree = ttk.Treeview(card_frame, columns=columns, show="headings")
        self.tree.heading("category", text="Category")
        self.tree.heading("component", text="Component Test")
        self.tree.heading("status", text="Result")
        self.tree.heading("details", text="Diagnostic Details")

        self.tree.column("category", width=110, anchor="w")
        self.tree.column("component", width=150, anchor="w")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("details", width=330, anchor="w")

        self.tree.tag_configure("PASS", foreground=COLOR_PASS)
        self.tree.tag_configure("FAIL", foreground=COLOR_FAIL)

        self.tree.pack(fill="both", expand=True)

        self.run_diagnostics()

    def run_diagnostics(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.status_lbl.config(text="Running diagnostics...", fg=ACCENT_BLUE)
        self.update_idletasks()

        tests = [
            self.check_cpu,
            self.check_memory,
            self.check_root_fs,
            self.check_network,
            self.check_graphics,
            self.check_package_manager
        ]

        passed = 0
        total = len(tests)

        for test_fn in tests:
            cat, comp, status, details = test_fn()
            self.tree.insert("", "end", values=(cat, comp, status, details), tags=(status,))
            if status == "PASS":
                passed += 1

        self.status_lbl.config(text=f"Diagnostics complete: {passed}/{total} Passed", fg=COLOR_PASS if passed == total else ACCENT_NEON)

    def check_cpu(self):
        try:
            cores = os.cpu_count()
            if cores and cores > 0:
                return "CPU", "Processor Cores", "PASS", f"Detected {cores} logical CPU core(s)"
            return "CPU", "Processor Cores", "FAIL", "Unable to detect CPU cores"
        except Exception as e:
            return "CPU", "Processor Cores", "FAIL", str(e)

    def check_memory(self):
        try:
            with open("/proc/meminfo", "r") as f:
                content = f.read()
                if "MemTotal" in content:
                    total_kb = int([line for line in content.split("\n") if "MemTotal" in line][0].split()[1])
                    total_mb = total_kb // 1024
                    return "Memory", "RAM Capacity", "PASS", f"Total RAM: {total_mb} MB"
            return "Memory", "RAM Capacity", "FAIL", "Could not read /proc/meminfo"
        except Exception as e:
            return "Memory", "RAM Capacity", "FAIL", str(e)

    def check_root_fs(self):
        try:
            total, used, free = shutil.disk_usage("/")
            free_gb = free / (1024**3)
            if free_gb > 0.5:
                return "Storage", "Root Filesystem", "PASS", f"Root partition accessible, {free_gb:.1f} GB free"
            return "Storage", "Root Filesystem", "FAIL", f"Low disk space: {free_gb:.1f} GB free"
        except Exception as e:
            return "Storage", "Root Filesystem", "FAIL", str(e)

    def check_network(self):
        try:
            s = socket.create_connection(("1.1.1.1", 53), timeout=2)
            s.close()
            return "Network", "Internet Connectivity", "PASS", "Connected to global network"
        except Exception:
            return "Network", "Internet Connectivity", "FAIL", "Network socket test failed / Offline"

    def check_graphics(self):
        display = os.environ.get("DISPLAY")
        if display:
            return "Display", "X11 Display Server", "PASS", f"Active DISPLAY={display}"
        return "Display", "X11 Display Server", "FAIL", "No active X11 display session"

    def check_package_manager(self):
        apt = shutil.which("apt-get") or shutil.which("dpkg")
        if apt:
            return "System", "Package Manager", "PASS", f"Found binary at {apt}"
        return "System", "Package Manager", "FAIL", "Neither apt-get nor dpkg available"

if __name__ == "__main__":
    app = LMGTestApp()
    app.mainloop()
