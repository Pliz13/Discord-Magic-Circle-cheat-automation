import threading
import time
import keyboard
import pyautogui
import math
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from screeninfo import get_monitors
import logging
import sys
import winsound  # For beep sound on Windows

# Global state
running = False
paused = False
loop_thread = None
click_thread = None
f5_click_thread = None
f5_clicker_running = False
overlay = None
overlay_enabled = None
delay_var = None
sound_enabled = None  # New global for beep sound toggle

# Status labels
status_label_movement_main = None
status_label_clicker_main = None
status_label_movement_overlay = None
status_label_clicker_overlay = None

log_text_widget = None  # Text widget for logging in GUI

DEFAULT_DELAY = 1.0

# Logging handler that writes to the Tkinter Text widget safely
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text_widget.configure(state='normal')
            self.text_widget.insert(tk.END, msg + '\n')
            self.text_widget.configure(state='disabled')
            self.text_widget.yview(tk.END)
        self.text_widget.after(0, append)

def beep_if_enabled():
    if sound_enabled.get():
        winsound.MessageBeep(winsound.MB_OK)

def action_sequence(get_w_delay):
    global running, paused
    logging.info("Movement thread started")
    while running:
        if paused:
            time.sleep(0.1)
            continue
        for _ in range(10):
            if not running:
                break
            while paused and running:
                time.sleep(0.1)
            logging.debug("Pressing 'w'")
            pyautogui.press('w')
            time.sleep(get_w_delay())
        if not running:
            break
        logging.debug("Pressing 'd'")
        pyautogui.press('d')
        for _ in range(10):
            if not running:
                break
            while paused and running:
                time.sleep(0.1)
            logging.debug("Pressing 's'")
            pyautogui.press('s')
            time.sleep(0.1)
    logging.info("Movement thread ended")

def auto_click():
    global running, paused
    logging.info("Auto click thread started")
    while running:
        if paused:
            time.sleep(0.1)
            continue
        pyautogui.click()
        time.sleep(0.01)
    logging.info("Auto click thread ended")

def auto_click_f5():
    global f5_clicker_running
    logging.info("F5 auto clicker thread started")
    while f5_clicker_running:
        pyautogui.click()
        time.sleep(0.01)
    logging.info("F5 auto clicker thread ended")

def toggle_f5_clicker():
    global f5_clicker_running, f5_click_thread
    beep_if_enabled()
    if not f5_clicker_running:
        logging.info("F5 auto clicker toggled ON")
        f5_clicker_running = True
        f5_click_thread = threading.Thread(target=auto_click_f5, daemon=True)
        f5_click_thread.start()
    else:
        logging.info("F5 auto clicker toggled OFF")
        f5_clicker_running = False
    update_status_labels()

def toggle_pause():
    global paused
    paused = not paused
    status = "Paused" if paused else "Resumed"
    logging.info(f"Movement & clicker {status}")
    update_status_labels()

def toggle_running(get_w_delay):
    global running, loop_thread, click_thread, paused
    beep_if_enabled()
    if not running:
        logging.info("Starting movement and auto click threads")
        running = True
        paused = False
        loop_thread = threading.Thread(target=action_sequence, args=(get_w_delay,), daemon=True)
        click_thread = threading.Thread(target=auto_click, daemon=True)
        loop_thread.start()
        click_thread.start()
    else:
        toggle_pause()
    update_status_labels()

def reset_loop():
    global running, paused, loop_thread, click_thread, f5_clicker_running
    beep_if_enabled()
    logging.info("FULL STOP: Resetting loop, stopping all threads & F5 clicker")
    running = False
    paused = False
    f5_clicker_running = False  # stop F5 clicker too
    if loop_thread and loop_thread.is_alive():
        loop_thread.join(timeout=1)
        logging.debug("Movement thread joined")
    if click_thread and click_thread.is_alive():
        click_thread.join(timeout=1)
        logging.debug("Auto click thread joined")
    loop_thread = None
    click_thread = None
    delay_var.set(DEFAULT_DELAY)
    update_status_labels()

def update_status_labels():
    if running and not paused:
        movement_status = "Running"
        movement_color = "green"
    elif paused:
        movement_status = "Paused"
        movement_color = "orange"
    else:
        movement_status = "Stopped"
        movement_color = "red"

    clicker_status = "Clicker: Enabled" if f5_clicker_running else "Clicker: Disabled"
    clicker_color = "green" if f5_clicker_running else "red"

    if status_label_movement_main:
        status_label_movement_main.config(text=f"Movement: {movement_status}", foreground=movement_color)
    if status_label_clicker_main:
        status_label_clicker_main.config(text=clicker_status, foreground=clicker_color)
    if status_label_movement_overlay:
        status_label_movement_overlay.config(text=f"Movement: {movement_status}", fg=movement_color)
    if status_label_clicker_overlay:
        status_label_clicker_overlay.config(text=clicker_status, fg=clicker_color)

def show_overlay():
    global overlay, overlay_enabled
    global status_label_movement_overlay, status_label_clicker_overlay

    if overlay:
        overlay.destroy()
        overlay = None

    if overlay_enabled.get():
        overlay = tk.Toplevel()
        overlay.overrideredirect(True)
        overlay.attributes('-topmost', True)
        overlay.attributes('-alpha', 0.9)
        overlay.configure(bg='black')

        container = tk.Frame(overlay, bg="black", padx=12, pady=12, bd=2, relief="ridge")
        container.pack()

        tk.Label(
            container,
            text="F5: Toggle Auto Clicker\nF6: Start/Pause Movement & Click\nF7: FULL STOP",
            font=("Segoe UI", 10),
            fg="white",
            bg="black",
            justify="left"
        ).pack(ipadx=10, ipady=5)

        status_frame = tk.Frame(container, bg='black')
        status_frame.pack(pady=(5, 5))

        status_label_movement_overlay = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="black"
        )
        status_label_movement_overlay.pack(side='left', padx=(0, 10))

        status_label_clicker_overlay = tk.Label(
            status_frame,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="black"
        )
        status_label_clicker_overlay.pack(side='left')

        ttk.Label(container, text="Delay Between 'W' Key Presses:", background='black', foreground='white').pack(pady=(5, 0))

        ttk.Scale(container, from_=0.1, to=5.0, orient='horizontal', length=200, variable=delay_var, bootstyle='info').pack(pady=5)

        x, y = pyautogui.position()
        monitor = next((m for m in get_monitors() if m.x <= x <= m.x + m.width and m.y <= y <= m.y + m.height), get_monitors()[0])
        overlay.update_idletasks()
        width = overlay.winfo_width()
        height = overlay.winfo_height()
        overlay.geometry(f"+{monitor.x + monitor.width - width - 20}+{monitor.y + monitor.height - height - 20}")

        update_status_labels()

def start_gui():
    global delay_var, overlay_enabled, sound_enabled
    global status_label_movement_main, status_label_clicker_main, log_text_widget

    root = ttk.Window(themename="superhero")
    root.title("Magic Circle Cheat")
    root.geometry("420x520")
    root.resizable(False, False)

    delay_var = tk.DoubleVar(value=DEFAULT_DELAY)
    overlay_enabled = tk.BooleanVar(value=False)
    sound_enabled = tk.BooleanVar(value=True)

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Delay Between 'W' Key Presses (in seconds):").pack(pady=(0, 10))

    slider = ttk.Scale(frame, from_=0.1, to=5.0, orient='horizontal', length=300, variable=delay_var, bootstyle='info')
    slider.pack()

    speed_label = ttk.Label(frame, text="Current W delay: 1.00s")
    speed_label.pack(pady=5)

    def update_label(value):
        speed_label.config(text=f"Current W delay: {float(value):.2f}s")

    slider.config(command=update_label)

    ttk.Label(frame, text="F5: Toggle Auto Clicker\nF6: Start/Pause Movement & Click\nF7: FULL STOP").pack(pady=10)

    status_frame = ttk.Frame(frame)
    status_frame.pack(pady=5)

    status_label_movement_main = ttk.Label(status_frame, text="Movement: Stopped", font=("Segoe UI", 10, "bold"))
    status_label_movement_main.pack(side='left', padx=(0, 10))

    status_label_clicker_main = ttk.Label(status_frame, text="Clicker: Disabled", font=("Segoe UI", 10, "bold"))
    status_label_clicker_main.pack(side='left')

    reset_button = ttk.Button(frame, text="FULL STOP", bootstyle="danger-outline", width=20, command=reset_loop)
    reset_button.pack(pady=10)

    show_overlay_check = ttk.Checkbutton(
        frame,
        text="Show controls overlay in screen corner under mouse",
        variable=overlay_enabled,
        command=show_overlay,
        bootstyle="info"
    )
    show_overlay_check.pack(pady=(5, 0))

    sound_checkbox = ttk.Checkbutton(
        frame,
        text="Enable beep sounds",
        variable=sound_enabled,
        bootstyle="info"
    )
    sound_checkbox.pack(pady=(5, 10))

    log_text_widget = tk.Text(frame, height=8, bg='black', fg='white', font=('Consolas', 9), state='disabled', wrap='none')
    log_text_widget.pack(fill='both', expand=True, pady=(10, 0))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler("magic_circle_cheat.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    text_handler = TextHandler(log_text_widget)
    text_handler.setFormatter(formatter)
    root_logger.addHandler(text_handler)

    def update_glow(event):
        mouse_x, mouse_y = event.x_root, event.y_root
        btn_x = reset_button.winfo_rootx()
        btn_y = reset_button.winfo_rooty()
        btn_w = reset_button.winfo_width()
        btn_h = reset_button.winfo_height()
        btn_cx = btn_x + btn_w / 2
        btn_cy = btn_y + btn_h / 2
        dist = math.sqrt((mouse_x - btn_cx) ** 2 + (mouse_y - btn_cy) ** 2)
        max_dist = 150
        intensity = max(0, min(1, (max_dist - dist) / max_dist))
        base_r, base_g, base_b = 220, 53, 69
        r = int(base_r + (255 - base_r) * intensity)
        g = int(base_g + (255 - base_g) * intensity)
        b = int(base_b + (255 - base_b) * intensity)
        color = f'#{r:02x}{g:02x}{b:02x}'
        style_name = "GlowDanger.TButton"
        ttk.Style().configure(style_name,
                              foreground="white",
                              background=color,
                              bordercolor=color,
                              focusthickness=3,
                              focuscolor=color,
                              relief="raised")
        reset_button.config(style=style_name)

    root.bind('<Motion>', update_glow)

    keyboard.add_hotkey('F5', toggle_f5_clicker)
    keyboard.add_hotkey('F6', lambda: toggle_running(lambda: float(delay_var.get())))
    keyboard.add_hotkey('F7', reset_loop)

    def on_close():
        logging.info("Application closing")
        reset_loop()
        if overlay:
            overlay.destroy()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    update_status_labels()
    logging.info("GUI started")
    root.mainloop()

if __name__ == "__main__":
    start_gui()
