<img width="1529" height="886" alt="image" src="https://github.com/user-attachments/assets/6c0e9282-fdb2-4d9d-a4f7-64ff82daf011" />



This is mainly made with chatGPT, feel free to use the code as you see fit 

# 🌀 Magic Circle Cheat — *Automation Tool for Discord's Magic Circle Activity*

A sleek Python-based automation tool designed specifically for **Magic Circle**, a mini-game found in **Discord Activities**. This tool simulates player movement and mouse clicking to help automate repetitive actions—useful for farming or grinding in the game loop.

---

## ✨ Features

- 🕹️ **Automated Movement**  
  Repeatedly presses `W`, `S`, and `D` in a programmed loop with adjustable delay.

- 🖱️ **Auto Clicker**  
  Rapid mouse clicking at the current cursor position—toggle anytime.

- 🌐 **On-Screen Overlay**  
  Floating HUD near your mouse showing status indicators and control info.

- 🎛️ **Adjustable Timing**  
  Control how fast movement loops run with a simple delay slider.

- 🔊 **Optional Beep Alerts** *(Windows only)*  
  Enables sound feedback when toggling features.

- 🧠 **Live Logging**  
  Logs all actions to a file, the console, and a live GUI view for debugging.

- 🖲️ **Global Hotkeys**

  | Hotkey | Action                        |
  |--------|-------------------------------|
  | F5     | Toggle auto clicker            |
  | F6     | Start/Pause movement & clicking (Garden Automation) |
  | F7     | FULL STOP (emergency reset)    |
  | F8     | Toggle Hump Mode (W/S spam)    |
  | F9     | Toggle Seizure Mode (random WASD spam) |
  | F10    | Toggle Overlay Window          |

---

## ⚙️ Requirements

- Python 3.8 or higher
- [pyautogui](https://pypi.org/project/pyautogui/)
- [keyboard](https://pypi.org/project/keyboard/)
- [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- [screeninfo](https://pypi.org/project/screeninfo/) (optional, if used)
- `winsound` (built-in on Windows)

### 🔧 Install dependencies

bash
pip install pyautogui keyboard ttkbootstrap screeninfo

🚀 How to Use

Open Magic Circle from Discord Activities.

download and run the .EXE from the relesses OR 

Run the script:
python magic_circle_cheat.py

Use the GUI or the following function keys to control the automation:

F5: Toggle Auto Clicker

F6: Start/Pause Garden Automation (movement + clicking)

F7: FULL STOP — immediately stop all automation

F8: Toggle Hump Mode (rapid W/S spam)

F9: Toggle Seizure Mode (random WASD spam)

F10: Toggle the on-screen overlay window

📁 Logs
The app generates a magic_circle_cheat.log file in the same directory.

Logs include detailed info on all actions and errors.

Logs are also shown live in the GUI.

⚠️ Disclaimer
This tool is provided for educational and personal use only. Automating inputs in games may violate Discord or game Terms of Service. Use responsibly and at your own risk.

💬 Feedback & Contributions
Feel free to open issues or pull requests to improve this tool.

Suggestions and feature requests are welcome!

📢 Acknowledgements
Thanks to the following libraries and tools used:

PyAutoGUI

Keyboard

ttkbootstrap

Colorama

