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
BORDER_COLOR = "#1e293b"
BUTTON_BG = "#1e293b"

class LMGDriverApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Driver — Hardware Driver Assistant")
        self.geometry("720x520")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG Hardware Driver Assistant",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Inspect kernel modules, GPU drivers, wireless firmware, and hardware support status",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Treeview
        card_frame = tk.Frame(self, bg=CARD_BG, padx=15, pady=15, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("device", "vendor", "driver", "status")
        self.tree = ttk.Treeview(card_frame, columns=columns, show="headings")
        self.tree.heading("device", text="Device Class")
        self.tree.heading("vendor", text="Hardware Vendor / Description")
        self.tree.heading("driver", text="In-Use Driver / Kernel Module")
        self.tree.heading("status", text="Driver Status")

        self.tree.column("device", width=120, anchor="w")
        self.tree.column("vendor", width=280, anchor="w")
        self.tree.column("driver", width=160, anchor="w")
        self.tree.column("status", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.scan_drivers()

    def scan_drivers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        lspci_k = subprocess.getoutput("lspci -k 2>/dev/null")
        devices = lspci_k.split("\n\n")

        for dev in devices:
            if dev.strip():
                lines = dev.strip().split("\n")
                first_line = lines[0]
                dev_class = first_line.split(":")[1].strip() if ":" in first_line else "PCI Device"
                vendor_desc = first_line.split(":", 2)[-1].strip() if first_line.count(":") >= 2 else first_line

                driver = "N/A / Generic"
                for l in lines:
                    if "Kernel driver in use:" in l:
                        driver = l.split(":")[1].strip()

                status = "Active" if driver != "N/A / Generic" else "Supported (Generic)"
                self.tree.insert("", "end", values=(dev_class[:20], vendor_desc[:45], driver, status))

if __name__ == "__main__":
    app = LMGDriverApp()
    app.mainloop()
