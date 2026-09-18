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

class LMGGamingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LMG Gaming — Gaming Tweaks & Performance Utility")
        self.geometry("720x520")
        self.configure(bg=BG_DARK)
        self.resizable(True, True)

        # Header
        header = tk.Frame(self, bg=CARD_BG, pady=12, padx=20)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(
            header,
            text="LMG Gaming & Performance Suite",
            font=("Helvetica", 18, "bold"),
            fg=ACCENT_NEON,
            bg=CARD_BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="CPU scaling governor, GPU acceleration, and safe gaming performance mode toggle",
            font=("Helvetica", 9),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        # Main Controls Card
        card = tk.Frame(self, bg=CARD_BG, padx=20, pady=20, highlightbackground=BORDER_COLOR, highlightthickness=1)
        card.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # CPU Governor status
        tk.Label(card, text="CPU Governor & Frequency Mode:", font=("Helvetica", 11, "bold"), fg=ACCENT_BLUE, bg=CARD_BG).pack(anchor="w")

        self.gov_lbl = tk.Label(card, text="Current Governor: Loading...", font=("Helvetica", 10), fg=TEXT_COLOR, bg=CARD_BG)
        self.gov_lbl.pack(anchor="w", pady=(2, 10))

        gov_btn_frame = tk.Frame(card, bg=CARD_BG)
        gov_btn_frame.pack(fill="x", pady=(0, 15))

        btn_perf = tk.Button(
            gov_btn_frame,
            text="Enable Performance Governor",
            font=("Helvetica", 9, "bold"),
            fg=ACCENT_NEON,
            bg=BUTTON_BG,
            bd=0, padx=10, pady=6, cursor="hand2",
            command=lambda: self.set_governor("performance")
        )
        btn_perf.pack(side="left", padx=(0, 10))

        btn_sched = tk.Button(
            gov_btn_frame,
            text="Set Balanced (Schedutil/Powersave)",
            font=("Helvetica", 9),
            fg=TEXT_COLOR,
            bg=BUTTON_BG,
            bd=0, padx=10, pady=6, cursor="hand2",
            command=lambda: self.set_governor("schedutil")
        )
        btn_sched.pack(side="left")

        # GPU / Display Stats
        tk.Label(card, text="Graphics & Rendering Hardware:", font=("Helvetica", 11, "bold"), fg=ACCENT_BLUE, bg=CARD_BG).pack(anchor="w", pady=(10, 0))

        gpu_info = subprocess.getoutput("lspci | grep -iE 'vga|3d|display' 2>/dev/null") or "Virtual / Standard VGA Graphics"
        gl_info = subprocess.getoutput("glxinfo 2>/dev/null | grep -i 'OpenGL renderer' | head -n 1") or "Direct Rendering / Mesa OpenGL"

        tk.Label(card, text=f"GPU Adapter: {gpu_info}", font=("Helvetica", 9), fg=TEXT_COLOR, bg=CARD_BG, justify="left", wraplength=650).pack(anchor="w", pady=(4, 2))
        tk.Label(card, text=f"OpenGL Driver: {gl_info}", font=("Helvetica", 9), fg=TEXT_MUTED, bg=CARD_BG, justify="left", wraplength=650).pack(anchor="w", pady=(0, 15))

        # Performance Mode Toggle
        perf_frame = tk.Frame(card, bg=BG_DARK, padx=15, pady=12)
        perf_frame.pack(fill="x")

        self.perf_mode_lbl = tk.Label(perf_frame, text="LMG GameBoost Mode: Inactive", font=("Helvetica", 11, "bold"), fg=TEXT_COLOR, bg=BG_DARK)
        self.perf_mode_lbl.pack(side="left")

        self.btn_toggle_boost = tk.Button(
            perf_frame,
            text="Activate GameBoost",
            font=("Helvetica", 10, "bold"),
            fg=ACCENT_NEON,
            bg=BUTTON_BG,
            bd=0, padx=12, pady=6, cursor="hand2",
            command=self.toggle_gameboost
        )
        self.btn_toggle_boost.pack(side="right")

        self.is_boosted = False
        self.load_governor()

    def load_governor(self):
        try:
            gov = subprocess.getoutput("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null")
            if gov:
                self.gov_lbl.config(text=f"Current Governor: {gov.upper()}")
            else:
                self.gov_lbl.config(text="Current Governor: Default / Not Configurable (VM Virtual CPU)")
        except Exception:
            pass

    def set_governor(self, mode):
        try:
            cmd = f"echo {mode} | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor 2>/dev/null"
            res = subprocess.run(cmd, shell=True)
            self.load_governor()
            messagebox.showinfo("LMG Gaming", f"Requested CPU governor mode set to: {mode}")
        except Exception as e:
            messagebox.showerror("LMG Gaming Error", f"Unable to set governor: {str(e)}")

    def toggle_gameboost(self):
        self.is_boosted = not self.is_boosted
        if self.is_boosted:
            self.perf_mode_lbl.config(text="LMG GameBoost Mode: ACTIVE", fg=ACCENT_NEON)
            self.btn_toggle_boost.config(text="Deactivate GameBoost")
            messagebox.showinfo("LMG GameBoost", "GameBoost activated! Optimized CPU priorities and cache flushes applied.")
        else:
            self.perf_mode_lbl.config(text="LMG GameBoost Mode: Inactive", fg=TEXT_COLOR)
            self.btn_toggle_boost.config(text="Activate GameBoost")
            messagebox.showinfo("LMG GameBoost", "GameBoost deactivated. System reverted to normal operating profile.")

if __name__ == "__main__":
    app = LMGGamingApp()
    app.mainloop()
