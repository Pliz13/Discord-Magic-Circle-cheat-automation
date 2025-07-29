<img width="1547" height="888" alt="image" src="https://github.com/user-attachments/assets/472bce71-76d7-4881-bd79-75d0d9a15e57" /> 


This is mainly made with chatGPT, feel free to use the code as you see fit 

Magic Circle Cheat — Automation Tool for Discord's Magic Circle Activity
A sleek Python-based automation tool designed specifically for Magic Circle, a mini-game found in Discord Activities. This tool simulates player movement and mouse clicking to help automate repetitive actions—useful for farming or grinding in the game loop.

✨ Features
🕹️ Automated Movement: Repeatedly presses W, S, and D in a programmed loop with adjustable delay.

🖱️ Auto Clicker: Clicks rapidly at the current mouse position—can be toggled on/off.

🌐 On-Screen Overlay: Floating status window near your mouse cursor shows live game control info.

🎛️ Adjustable Timing: Real-time slider to control delay between movement key presses.

🔊 Optional Beep Alerts: Audio feedback (Windows-only) for toggles and stops.

🧠 Live Logging: Logs actions to a file, console, and a built-in GUI window.

🖲️ Global Hotkeys:

F5: Toggle auto clicker

F6: Start/Pause movement and clicking

F7: FULL STOP (emergency reset)

⚙️ Requirements
Python 3.8+

pyautogui

keyboard

ttkbootstrap

screeninfo

winsound (for Windows beep sounds)

Install dependencies:

bash
Copy
Edit
pip install pyautogui keyboard ttkbootstrap screeninfo
🚀 How to Use
Launch the Magic Circle activity in Discord.

Run this script:

bash
Copy
Edit
python magic_circle_cheat.py
Use the GUI or hotkeys to control automation.

⚠️ Disclaimer
This tool is intended for educational and personal use only. Using automation in online games may violate Discord’s or the game’s Terms of Service. Use at your own risk.
