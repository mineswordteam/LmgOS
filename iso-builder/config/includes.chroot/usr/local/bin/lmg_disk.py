#!/usr/bin/env python3
import sys
import os
import subprocess
import tkinter as tk
from tkinter import ttk

BG_DARK = "#0b0f19"
CARD_BG = "#161e2e"
TEXT_COLOR = "#f8fafc"
TEXT_MUTED = "#94a3b8"
ACCENT_BLUE = "#38bdf8"
ACCENT_NEON = "#00f0ff"
BORDER_COLOR = "#1e293b"

class LMGDiskApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Disk — Storage & Partition Utility")
        self.geometry("740x520")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG Disk Manager",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Storage devices, partitions, mountpoints and filesystem usage",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Table
        card_frame = tk.Frame(self, bg=CARD_BG, padx=15, pady=15, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("filesystem", "type", "size", "used", "avail", "use_pct", "mount")
        self.tree = ttk.Treeview(card_frame, columns=columns, show="headings")

        self.tree.heading("filesystem", text="Filesystem")
        self.tree.heading("type", text="Type")
        self.tree.heading("size", text="Size")
        self.tree.heading("used", text="Used")
        self.tree.heading("avail", text="Avail")
        self.tree.heading("use_pct", text="Use %")
        self.tree.heading("mount", text="Mounted On")

        self.tree.column("filesystem", width=140, anchor="w")
        self.tree.column("type", width=70, anchor="center")
        self.tree.column("size", width=70, anchor="center")
        self.tree.column("used", width=70, anchor="center")
        self.tree.column("avail", width=70, anchor="center")
        self.tree.column("use_pct", width=60, anchor="center")
        self.tree.column("mount", width=160, anchor="w")

        self.tree.pack(fill="both", expand=True)

        self.load_disks()

    def load_disks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        df_out = subprocess.getoutput("df -hT -x tmpfs -x devtmpfs -x squashfs 2>/dev/null")
        lines = df_out.strip().split("\n")
        if len(lines) > 1:
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 7:
                    fs, fstype, size, used, avail, use_pct, mount = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
                    self.tree.insert("", "end", values=(fs, fstype, size, used, avail, use_pct, mount))

if __name__ == "__main__":
    app = LMGDiskApp()
    app.mainloop()
