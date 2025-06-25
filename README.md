# keylogger_project
Encrypted Keylogger with Simulated Data Exfiltration

## Objective
Demonstrates a keylogger that captures keystrokes, encrypts logs, stores them with timestamps, and simulates exfiltration.

## Tools
Python, pynput, cryptography, base64, datetime, time, Flask (optional)

## Features
- Real-time keylogging
- Encrypted log storage with Fernet
- Base64 encoding
- Timestamped logs
- Simulated exfiltration (localhost)
- Optional startup persistence
- Kill switch (Ctrl+Shift+Q)
