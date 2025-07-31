import threading
import time
import keyboard
import pyautogui
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys
import logging
from colorama import init as colorama_init, Fore, Style
import random

# Initialize colorama for Windows terminal colors
colorama_init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.WHITE)
        msg = super().format(record)
        return f"{color}{msg}{Style.RESET_ALL}"


class TkinterLogger(logging.Handler):
    LEVEL_COLORS = {
        logging.DEBUG: "cyan",
        logging.INFO: "green",
        logging.WARNING: "orange",
        logging.ERROR: "red",
        logging.CRITICAL: "red4",
    }

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        for level, color in self.LEVEL_COLORS.items():
            self.text_widget.tag_configure(level, foreground=color)

    def emit(self, record):
        msg = self.format(record) + "\n"
        color_tag = record.levelno

        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg, color_tag)
            self.text_widget.configure(state='disabled')
            self.text_widget.see(tk.END)

        self.text_widget.after(0, append)


class Controller:
    def __init__(self, delay_var, hump_speed_var, seizure_speed_var, log_callback=None):
        self.running = False
        self.paused = False
        self.f5_clicker_running = False
        self.hump_running = False
        self.seizure_running = False

        self.delay_var = delay_var
        self.hump_speed_var = hump_speed_var
        self.seizure_speed_var = seizure_speed_var

        self.loop_thread = None
        self.click_thread = None
        self.f5_click_thread = None
        self.hump_thread = None
        self.seizure_thread = None

        self.log_callback = log_callback

    def log(self, level, message):
        if self.log_callback:
            self.log_callback(level, message)
        else:
            logging.getLogger().log(level, message)

    def action_sequence(self):
        self.log(logging.INFO, "Movement thread started")
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            for _ in range(10):
                if not self.running:
                    break
                while self.paused and self.running:
                    time.sleep(0.1)
                pyautogui.press('w')
                time.sleep(self.delay_var.get())
            if not self.running:
                break
            pyautogui.press('d')
            for _ in range(10):
                if not self.running:
                    break
                while self.paused and self.running:
                    time.sleep(0.1)
                pyautogui.press('s')
                time.sleep(0.1)
        self.log(logging.INFO, "Movement thread ended")

    def auto_click(self):
        self.log(logging.INFO, "Auto click thread started")
        while self.running:
            if self.paused:
                time.sleep(0.1)
                continue
            pyautogui.click()
            time.sleep(0.01)
        self.log(logging.INFO, "Auto click thread ended")

    def auto_click_f5(self):
        self.log(logging.INFO, "F5 auto clicker thread started")
        while self.f5_clicker_running:
            pyautogui.click()
            time.sleep(0.01)
        self.log(logging.INFO, "F5 auto clicker thread ended")

    # Original hump method restored
    def hump_action(self):
        self.log(logging.INFO, "Hump thread started")
        while self.hump_running:
            pyautogui.press('w')
            pyautogui.press('s')
            time.sleep(self.hump_speed_var.get())
        self.log(logging.INFO, "Hump thread ended")

    # Original seizure method restored
    def seizure_mode(self):
        buttons = ['w', 'a', 's', 'd']
        self.log(logging.INFO, "Seizure mode thread started")
        while self.seizure_running:
            key = buttons[random.randint(0, 3)]
            pyautogui.press(key)
            time.sleep(self.seizure_speed_var.get())
        self.log(logging.INFO, "Seizure mode thread ended")

    def toggle_f5_clicker(self):
        if not self.f5_clicker_running:
            self.log(logging.INFO, "F5 auto clicker toggled ON")
            self.f5_clicker_running = True
            self.f5_click_thread = threading.Thread(target=self.auto_click_f5, daemon=True)
            self.f5_click_thread.start()
        else:
            self.log(logging.INFO, "F5 auto clicker toggled OFF")
            self.f5_clicker_running = False

    def toggle_running(self):
        if not self.running:
            self.log(logging.INFO, "Starting movement and auto click threads")
            self.running = True
            self.paused = False
            self.loop_thread = threading.Thread(target=self.action_sequence, daemon=True)
            self.click_thread = threading.Thread(target=self.auto_click, daemon=True)
            self.loop_thread.start()
            self.click_thread.start()
        else:
            self.paused = not self.paused
            state = "Paused" if self.paused else "Resumed"
            self.log(logging.INFO, f"Garden Automation {state}")

    def toggle_hump(self):
        if not self.hump_running:
            self.log(logging.INFO, "Hump spam toggled ON")
            self.hump_running = True
            self.hump_thread = threading.Thread(target=self.hump_action, daemon=True)
            self.hump_thread.start()
        else:
            self.log(logging.INFO, "Hump spam toggled OFF")
            self.hump_running = False

    def toggle_seizure(self):
        if not self.seizure_running:
            self.log(logging.INFO, "Seizure mode toggled ON")
            self.seizure_running = True
            self.seizure_thread = threading.Thread(target=self.seizure_mode, daemon=True)
            self.seizure_thread.start()
        else:
            self.log(logging.INFO, "Seizure mode toggled OFF")
            self.seizure_running = False

    def reset_all(self):
        self.log(logging.INFO, "FULL STOP: Resetting all")
        self.running = False
        self.paused = False
        self.f5_clicker_running = False
        self.hump_running = False
        self.seizure_running = False


class Overlay(tk.Toplevel):
    def __init__(self, parent, controller, delay_var, hump_speed_var, seizure_speed_var):
        super().__init__(parent)
        self.controller = controller
        self.delay_var = delay_var
        self.hump_speed_var = hump_speed_var
        self.seizure_speed_var = seizure_speed_var

        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.85)
        self.configure(bg='black')

        container = tk.Frame(self, bg="black", padx=15, pady=15, bd=2, relief="ridge")
        container.pack()

        label = tk.Label(
            container,
            text=(
                "F5: Toggle Auto Clicker\n"
                "F6: Garden Automation\n"
                "F7: FULL STOP\n"
                "F8: Toggle Hump (W & S spam)\n"
                "F9: Toggle Seizure Mode (random WASD spam)"
            ),
            font=("Segoe UI", 10),
            fg="white",
            bg="black",
            justify="left",
        )
        label.pack(ipadx=5, ipady=5)

        # Status labels frame
        self.status_frame = tk.Frame(container, bg='black')
        self.status_frame.pack(pady=8)

        self.status_movement = tk.Label(self.status_frame, font=("Segoe UI", 10, "bold"), fg="white", bg="black")
        self.status_movement.pack(side="left", padx=(0, 10))

        self.status_clicker = tk.Label(self.status_frame, font=("Segoe UI", 10, "bold"), fg="white", bg="black")
        self.status_clicker.pack(side="left", padx=(0, 10))

        self.status_hump = tk.Label(self.status_frame, font=("Segoe UI", 10, "bold"), fg="white", bg="black")
        self.status_hump.pack(side="left", padx=(0, 10))

        self.status_seizure = tk.Label(self.status_frame, font=("Segoe UI", 10, "bold"), fg="white", bg="black")
        self.status_seizure.pack(side="left")

        # Sliders on overlay

        ttk.Label(container, text="Delay Between 'W' Key Presses (seconds):", background='black', foreground='white').pack()
        self.delay_scale = ttk.Scale(container, from_=0.1, to=5.0, orient="horizontal", length=220, variable=self.delay_var, bootstyle="info")
        self.delay_scale.pack(pady=5)

        ttk.Label(container, text="Hump Speed (W/S delay):", background='black', foreground='white').pack()
        self.hump_speed_scale = ttk.Scale(container, from_=0.001, to=0.2, orient="horizontal", length=220, variable=self.hump_speed_var, bootstyle="info")
        self.hump_speed_scale.pack(pady=5)

        ttk.Label(container, text="Seizure Speed (WASD spam delay):", background='black', foreground='white').pack()
        self.seizure_speed_scale = ttk.Scale(container, from_=0.001, to=0.2, orient="horizontal", length=220, variable=self.seizure_speed_var, bootstyle="info")
        self.seizure_speed_scale.pack(pady=5)

        self.position_overlay()
        self.update_status()
        self.update_loop()

    def position_overlay(self):
        padding_x = 20
        padding_y = 40
        self.geometry(f"+{padding_x}+{padding_y}")

    def update_status(self):
        # Movement status renamed to Garden Automation status
        if self.controller.running and not self.controller.paused:
            mov_text = "Garden Automation: Running"
            mov_color = "lime"
        elif self.controller.paused:
            mov_text = "Garden Automation: Paused"
            mov_color = "orange"
        else:
            mov_text = "Garden Automation: Stopped"
            mov_color = "red"

        # Clicker status
        if self.controller.f5_clicker_running:
            clk_text = "Clicker: Enabled"
            clk_color = "lime"
        else:
            clk_text = "Clicker: Disabled"
            clk_color = "red"

        # Hump status
        if self.controller.hump_running:
            hump_text = "Hump: Enabled"
            hump_color = "lime"
        else:
            hump_text = "Hump: Disabled"
            hump_color = "red"

        # Seizure status
        if self.controller.seizure_running:
            seiz_text = "Seizure: Enabled"
            seiz_color = "lime"
        else:
            seiz_text = "Seizure: Disabled"
            seiz_color = "red"

        self.status_movement.config(text=mov_text, fg=mov_color)
        self.status_clicker.config(text=clk_text, fg=clk_color)
        self.status_hump.config(text=hump_text, fg=hump_color)
        self.status_seizure.config(text=seiz_text, fg=seiz_color)

    def update_loop(self):
        self.update_status()
        self.after(500, self.update_loop)  # update status every 0.5 seconds


class MagicCircleApp:
    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("Magic Circle Cheat")
        self.root.geometry("480x560")
        self.root.resizable(False, False)

        # Control variables
        self.delay_var = tk.DoubleVar(value=1.0)  # delay for W key press
        self.hump_speed_var = tk.DoubleVar(value=0.01)
        self.seizure_speed_var = tk.DoubleVar(value=0.01)

        # Setup controller
        self.controller = Controller(self.delay_var, self.hump_speed_var, self.seizure_speed_var, log_callback=self.log_message)

        # UI Setup
        self.create_widgets()

        # Overlay starts CLOSED, do NOT create it yet
        self.overlay = None

        # Register hotkeys
        keyboard.add_hotkey('f5', self.controller.toggle_f5_clicker)
        keyboard.add_hotkey('f6', self.controller.toggle_running)
        keyboard.add_hotkey('f7', self.full_stop)
        keyboard.add_hotkey('f8', self.controller.toggle_hump)
        keyboard.add_hotkey('f9', self.controller.toggle_seizure)
        keyboard.add_hotkey('f10', self.toggle_overlay)  # NEW: Toggle overlay on/off

        # Mainloop close protocol
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def create_widgets(self):
        title = ttk.Label(self.root, text="Magic Circle Cheat", font=("Segoe UI", 24, "bold"))
        title.pack(pady=10)

        info_label = ttk.Label(self.root,
                               text="Hotkeys:\nF5 - Toggle Auto Clicker\nF6 - Garden Automation\nF7 - FULL STOP\nF8 - Toggle Hump (W & S spam)\nF9 - Toggle Seizure Mode (random WASD spam)\nF10 - Toggle Overlay",
                               justify="left")
        info_label.pack(pady=10)

        # Sliders on main window
        ttk.Label(self.root, text="Delay Between 'W' Key Presses (seconds):").pack()
        self.delay_scale = ttk.Scale(self.root, from_=0.1, to=5.0, orient="horizontal", length=400, variable=self.delay_var, bootstyle="info")
        self.delay_scale.pack(pady=10)

        ttk.Label(self.root, text="Hump Speed (W/S delay):").pack()
        self.hump_speed_scale = ttk.Scale(self.root, from_=0.001, to=0.2, orient="horizontal", length=400, variable=self.hump_speed_var, bootstyle="info")
        self.hump_speed_scale.pack(pady=10)

        ttk.Label(self.root, text="Seizure Speed (WASD spam delay):").pack()
        self.seizure_speed_scale = ttk.Scale(self.root, from_=0.001, to=0.2, orient="horizontal", length=400, variable=self.seizure_speed_var, bootstyle="info")
        self.seizure_speed_scale.pack(pady=10)

        # Log box
        log_label = ttk.Label(self.root, text="Log Output:")
        log_label.pack()
        self.log_text = tk.Text(self.root, height=10, state='disabled', bg='black', fg='white', font=("Consolas", 10))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Setup logger for the text widget
        self.tk_logger = TkinterLogger(self.log_text)
        self.tk_logger.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(self.tk_logger)
        logging.getLogger().setLevel(logging.DEBUG)

    def log_message(self, level, message):
        logging.log(level, message)

    def toggle_overlay(self):
        if self.overlay is None or not self.overlay.winfo_exists():
            self.overlay = Overlay(self.root, self.controller, self.delay_var, self.hump_speed_var, self.seizure_speed_var)
        else:
            self.overlay.destroy()
            self.overlay = None

    def full_stop(self):
        self.controller.reset_all()

    def exit_app(self):
        self.full_stop()
        if self.overlay is not None:
            self.overlay.destroy()
        self.root.destroy()
        sys.exit()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MagicCircleApp()
    app.run()
