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

class LMGRAMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG RAM — System Memory Monitor & Flush")
        self.geometry("700x540")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG RAM Monitor & Optimizer",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Real-time physical memory and swap usage analysis",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Memory Progress Cards
        mem_card = tk.Frame(self, bg=CARD_BG, padx=15, pady=15, highlightbackground=BORDER_COLOR, highlightthickness=1)
        mem_card.pack(fill="x", padx=15, pady=(0, 10))

        self.ram_lbl = tk.Label(mem_card, text="RAM Usage: Loading...", font=("Helvetica", 11, "bold"), fg=TEXT_COLOR, bg=CARD_BG)
        self.ram_lbl.pack(anchor="w")

        self.ram_bar = ttk.Progressbar(mem_card, orient="horizontal", mode="determinate")
        self.ram_bar.pack(fill="x", pady=5)

        self.ram_details_lbl = tk.Label(mem_card, text="", font=("Helvetica", 9), fg=TEXT_MUTED, bg=CARD_BG)
        self.ram_details_lbl.pack(anchor="w")

        # Swap Card
        swap_card = tk.Frame(self, bg=CARD_BG, padx=15, pady=10, highlightbackground=BORDER_COLOR, highlightthickness=1)
        swap_card.pack(fill="x", padx=15, pady=(0, 10))

        self.swap_lbl = tk.Label(swap_card, text="Swap Usage: Loading...", font=("Helvetica", 10, "bold"), fg=TEXT_COLOR, bg=CARD_BG)
        self.swap_lbl.pack(anchor="w")

        self.swap_bar = ttk.Progressbar(swap_card, orient="horizontal", mode="determinate")
        self.swap_bar.pack(fill="x", pady=5)

        # Process List & Actions
        proc_card = tk.Frame(self, bg=CARD_BG, padx=15, pady=10, highlightbackground=BORDER_COLOR, highlightthickness=1)
        proc_card.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        top_bar = tk.Frame(proc_card, bg=CARD_BG)
        top_bar.pack(fill="x", pady=(0, 5))

        tk.Label(top_bar, text="Top Memory-Consuming Processes", font=("Helvetica", 11, "bold"), fg=ACCENT_BLUE, bg=CARD_BG).pack(side="left")

        btn_flush = tk.Button(
            top_bar,
            text="Safe Clean Caches",
            font=("Helvetica", 9, "bold"),
            fg=ACCENT_NEON,
            bg=BUTTON_BG,
            activebackground=CARD_BG,
            activeforeground=ACCENT_NEON,
            bd=0,
            padx=10,
            pady=4,
            cursor="hand2",
            command=self.safe_clean_caches
        )
        btn_flush.pack(side="right")

        # Treeview for processes
        columns = ("pid", "user", "mem_pct", "command")
        self.proc_tree = ttk.Treeview(proc_card, columns=columns, show="headings", height=8)
        self.proc_tree.heading("pid", text="PID")
        self.proc_tree.heading("user", text="User")
        self.proc_tree.heading("mem_pct", text="RAM %")
        self.proc_tree.heading("command", text="Command")

        self.proc_tree.column("pid", width=70, anchor="center")
        self.proc_tree.column("user", width=90, anchor="center")
        self.proc_tree.column("mem_pct", width=80, anchor="center")
        self.proc_tree.column("command", width=380, anchor="w")

        self.proc_tree.pack(fill="both", expand=True)

        self.update_stats()

    def update_stats(self):
        try:
            # Memory info
            with open("/proc/meminfo", "r") as f:
                meminfo = {}
                for line in f:
                    parts = line.split(":")
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val_str = parts[1].strip().split()[0]
                        if val_str.isdigit():
                            meminfo[key] = int(val_str)

            total_kb = meminfo.get("MemTotal", 1)
            free_kb = meminfo.get("MemFree", 0)
            avail_kb = meminfo.get("MemAvailable", free_kb)
            used_kb = total_kb - avail_kb

            swap_total_kb = meminfo.get("SwapTotal", 0)
            swap_free_kb = meminfo.get("SwapFree", 0)
            swap_used_kb = swap_total_kb - swap_free_kb

            ram_pct = (used_kb / total_kb) * 100
            self.ram_bar["value"] = ram_pct
            self.ram_lbl.config(text=f"RAM Usage: {ram_pct:.1f}% used")
            self.ram_details_lbl.config(
                text=f"Total: {total_kb/1024:.0f} MB | Used: {used_kb/1024:.0f} MB | Available: {avail_kb/1024:.0f} MB"
            )

            if swap_total_kb > 0:
                swap_pct = (swap_used_kb / swap_total_kb) * 100
                self.swap_bar["value"] = swap_pct
                self.swap_lbl.config(text=f"Swap Usage: {swap_pct:.1f}% ({swap_used_kb/1024:.0f} MB / {swap_total_kb/1024:.0f} MB)")
            else:
                self.swap_bar["value"] = 0
                self.swap_lbl.config(text="Swap Usage: Disabled / None")

            # Update Process list
            for row in self.proc_tree.get_children():
                self.proc_tree.delete(row)

            ps_output = subprocess.getoutput("ps aux --sort=-%mem | awk 'NR>1 {print $2, $1, $4, $11}' | head -n 10")
            for line in ps_output.strip().split("\n"):
                if line:
                    parts = line.split(maxsplit=3)
                    if len(parts) == 4:
                        self.proc_tree.insert("", "end", values=parts)

        except Exception as e:
            pass

        self.after(3000, self.update_stats)

    def safe_clean_caches(self):
        try:
            # Safe drop caches (pagecache)
            cmd = "sudo sync && sudo sysctl -w vm.drop_caches=1"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if res.returncode == 0:
                messagebox.showinfo("LMG RAM", "Pagecache dropped successfully. Reclaimed cached memory safely.")
            else:
                # Try without sudo if already root or fail gracefully
                res_alt = subprocess.run("sync; echo 1 > /proc/sys/drop_caches 2>/dev/null", shell=True)
                if res_alt.returncode == 0:
                    messagebox.showinfo("LMG RAM", "Memory cache flushed successfully.")
                else:
                    messagebox.showwarning("Permission Required", "Administrative privileges required to flush system cache.")
        except Exception as e:
            messagebox.showerror("Error", f"Flush operation failed: {str(e)}")

if __name__ == "__main__":
    app = LMGRAMApp()
    app.mainloop()
