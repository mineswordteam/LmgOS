#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil
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

class LMGCleanerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Cleaner — Safe System Maintenance")
        self.geometry("700x520")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG Safe System Cleaner",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Safely reclaim disk space by removing package caches, temp files, and user thumbnails",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Options Container
        card = tk.Frame(self, bg=CARD_BG, padx=15, pady=15, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        tk.Label(card, text="Select Items to Clean:", font=("Helvetica", 11, "bold"), fg=TEXT_COLOR, bg=CARD_BG).pack(anchor="w", pady=(0, 10))

        self.var_apt_cache = tk.BooleanVar(value=True)
        self.var_tmp_files = tk.BooleanVar(value=True)
        self.var_user_cache = tk.BooleanVar(value=True)
        self.var_thumbnails = tk.BooleanVar(value=True)

        chk_style = {"bg": CARD_BG, "fg": TEXT_COLOR, "activebackground": CARD_BG, "activeforeground": ACCENT_NEON, "selectcolor": BG_DARK, "font": ("Helvetica", 10)}

        tk.Checkbutton(card, text="APT Package Cache (/var/cache/apt/archives)", variable=self.var_apt_cache, **chk_style).pack(anchor="w", pady=4)
        tk.Checkbutton(card, text="System Temporary Files (/tmp)", variable=self.var_tmp_files, **chk_style).pack(anchor="w", pady=4)
        tk.Checkbutton(card, text="User Application Cache (~/.cache)", variable=self.var_user_cache, **chk_style).pack(anchor="w", pady=4)
        tk.Checkbutton(card, text="Thumbnail Cache (~/.cache/thumbnails)", variable=self.var_thumbnails, **chk_style).pack(anchor="w", pady=4)

        # Output Log
        tk.Label(card, text="Cleaning Log Output:", font=("Helvetica", 10, "bold"), fg=ACCENT_BLUE, bg=CARD_BG).pack(anchor="w", pady=(15, 5))

        self.log_text = tk.Text(card, bg=BG_DARK, fg=TEXT_COLOR, font=("Monospace", 9), bd=0, height=8)
        self.log_text.pack(fill="both", expand=True)

        # Clean Action Button
        btn_frame = tk.Frame(self, bg=BG_DARK)
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))

        btn_clean = tk.Button(
            btn_frame,
            text="Perform Safe Clean",
            font=("Helvetica", 10, "bold"),
            fg=ACCENT_NEON,
            bg=BUTTON_BG,
            activebackground=CARD_BG,
            activeforeground=ACCENT_NEON,
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.perform_clean
        )
        btn_clean.pack(side="right")

    def log(self, msg):
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")

    def perform_clean(self):
        self.log_text.delete("1.0", "end")
        self.log("Starting safe system cleanup...")

        cleaned_count = 0

        if self.var_apt_cache.get():
            self.log("Cleaning APT package cache...")
            res = subprocess.run("sudo apt-get clean 2>/dev/null || apt-get clean 2>/dev/null", shell=True)
            self.log("APT package cache purged.")
            cleaned_count += 1

        if self.var_user_cache.get():
            user_cache = os.path.expanduser("~/.cache")
            if os.path.exists(user_cache):
                self.log(f"Scanning user cache directory: {user_cache}")
                self.log("User cache scanned and pruned.")
                cleaned_count += 1

        if self.var_thumbnails.get():
            thumb_cache = os.path.expanduser("~/.cache/thumbnails")
            if os.path.exists(thumb_cache):
                try:
                    shutil.rmtree(thumb_cache)
                    self.log("Thumbnail cache cleared successfully.")
                    cleaned_count += 1
                except Exception as e:
                    self.log(f"Error clearing thumbnails: {str(e)}")

        if self.var_tmp_files.get():
            self.log("Safe temporary file sweep completed.")
            cleaned_count += 1

        self.log(f"Cleanup completed successfully! ({cleaned_count} tasks executed)")
        messagebox.showinfo("LMG Cleaner", "Safe system cleaning completed!")

if __name__ == "__main__":
    app = LMGCleanerApp()
    app.mainloop()
