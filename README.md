<img width="1547" height="888" alt="image" src="https://github.com/user-attachments/assets/472bce71-76d7-4881-bd79-75d0d9a15e57" /> 


This is mainly made with chatGPT, feel free to use the code as you see fit 

# 🌀 Magic Circle Cheat — *Automation Tool for Discord's Magic Circle Activity*

A sleek Python-based automation tool designed specifically for **Magic Circle**, a mini-game found in **Discord Activities**. This tool simulates player movement and mouse clicking to help automate repetitive actions—useful for farming or grinding in the game loop.

---

## ✨ Features

- 🕹️ **Automated Movement**  
  Repeatedly presses `W`, `S`, and `D` in a programmed loop with adjustable delay.

- 🖱️ **Auto Clicker**  
  Rapid mouse clicking at the current cursor position—toggle it anytime.

- 🌐 **On-Screen Overlay**  
  Floating HUD near your mouse showing status indicators and control info.

- 🎛️ **Adjustable Timing**  
  Control how fast movement loops run with a simple delay slider.

- 🔊 **Optional Beep Alerts** *(Windows only)*  
  Enables sound feedback when toggling features.

- 🧠 **Live Logging**  
  Logs all actions to a file, the console, and a live GUI view for debugging.

- 🖲️ **Global Hotkeys**

F5 - Toggle auto clicker
F6 - Start/Pause movement & clicking
F7 - FULL STOP (emergency reset)


---

## ⚙️ Requirements (only if you run the .py file)

- Python 3.8+
- [pyautogui](https://pypi.org/project/pyautogui/)
- [keyboard](https://pypi.org/project/keyboard/)
- [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- [screeninfo](https://pypi.org/project/screeninfo/)
- `winsound` (Built-in on Windows)

### 🔧 Install dependencies

pip install pyautogui keyboard ttkbootstrap screeninfo 

🚀 How to Use
Open Magic Circle from Discord Activities.

Run the script:

python magic_circle_cheat.py

Use the GUI or function keys (F5, F6, F7) to control the automation.

📁 Logs
A magic_circle_cheat.log file will be generated in the same directory to keep a detailed record of all activity and errors.

⚠️ Disclaimer
This tool is provided for educational and personal use only. Automating inputs in games may violate the Terms of Service of Discord or the game itself. Use at your own risk.

💬 Feedback & Contributions
Feel free to open issues or pull requests to improve this tool. Suggestions are welcome!


Let me know if you'd like:
- Badges (e.g. Python version, license)
- A license file
- Screenshot or GIF section
- GitHub Actions for packaging or validation


