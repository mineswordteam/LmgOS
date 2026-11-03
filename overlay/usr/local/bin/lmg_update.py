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

class LMGUpdateApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Update — Package Manager")
        self.geometry("740x540")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG Software Update Manager",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Real Debian 13.6 (Trixie) package index query and upgrade manager",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Top Bar
        top_bar = tk.Frame(self, bg=BG_DARK)
        top_bar.pack(fill="x", padx=15, pady=(0, 10))

        self.status_lbl = tk.Label(top_bar, text="Click 'Check Updates' to query package repositories.", font=("Helvetica", 10), fg=TEXT_COLOR, bg=BG_DARK)
        self.status_lbl.pack(side="left")

        btn_refresh = tk.Button(
            top_bar,
            text="Check Updates",
            font=("Helvetica", 9, "bold"),
            fg=ACCENT_NEON,
            bg=BUTTON_BG,
            bd=0, padx=10, pady=5, cursor="hand2",
            command=self.check_updates
        )
        btn_refresh.pack(side="right", padx=(5, 0))

        btn_upgrade = tk.Button(
            top_bar,
            text="Apply Upgrades",
            font=("Helvetica", 9, "bold"),
            fg=ACCENT_BLUE,
            bg=BUTTON_BG,
            bd=0, padx=10, pady=5, cursor="hand2",
            command=self.apply_upgrades
        )
        btn_upgrade.pack(side="right")

        # Treeview
        card_frame = tk.Frame(self, bg=CARD_BG, padx=15, pady=15, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("pkg", "curr_ver", "new_ver", "arch")
        self.tree = ttk.Treeview(card_frame, columns=columns, show="headings")
        self.tree.heading("pkg", text="Package Name")
        self.tree.heading("curr_ver", text="Installed Version")
        self.tree.heading("new_ver", text="Candidate Version")
        self.tree.heading("arch", text="Architecture")

        self.tree.column("pkg", width=220, anchor="w")
        self.tree.column("curr_ver", width=160, anchor="w")
        self.tree.column("new_ver", width=160, anchor="w")
        self.tree.column("arch", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.check_updates()

    def check_updates(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.status_lbl.config(text="Querying APT package repositories...", fg=ACCENT_BLUE)
        self.update_idletasks()

        # Run apt list --upgradable
        res = subprocess.getoutput("apt list --upgradable 2>/dev/null")
        lines = res.strip().split("\n")

        count = 0
        for line in lines:
            if "/" in line and "[" in line:
                try:
                    parts = line.split()
                    pkg_info = parts[0].split("/")
                    pkg_name = pkg_info[0]
                    new_ver = parts[1]
                    arch = pkg_info[1] if len(pkg_info) > 1 else "amd64"
                    curr_ver = "Installed"
                    if "installed:" in line:
                        curr_ver = line.split("installed:")[1].replace("]", "").strip()

                    self.tree.insert("", "end", values=(pkg_name, curr_ver, new_ver, arch))
                    count += 1
                except Exception:
                    pass

        if count == 0:
            self.status_lbl.config(text="System is completely up to date. No pending updates found.", fg="#22c55e")
        else:
            self.status_lbl.config(text=f"Found {count} update(s) available.", fg=ACCENT_NEON)

    def apply_upgrades(self):
        try:
            cmd = "x-terminal-emulator -e 'sudo apt-get update && sudo apt-get dist-upgrade'"
            subprocess.Popen(cmd, shell=True)
            messagebox.showinfo("LMG Update", "Opened update terminal session for package upgrade.")
        except Exception as e:
            messagebox.showerror("LMG Update Error", f"Unable to launch terminal upgrade: {str(e)}")

if __name__ == "__main__":
    app = LMGUpdateApp()
    app.mainloop()
