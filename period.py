import time
import random
import keyboard
import threading
import subprocess
import psutil
import pygetwindow as gw
import win32gui
import win32con
import win32console
import os

# For generating current requirements.txt - author:
# pip freeze > requirements.txt

# Globals to control thread flow
exit_event = threading.Event()
trigger_event = threading.Event()

def bring_self_to_front():
    """Bring the current console window to the foreground."""
    console_hwnd = win32console.GetConsoleWindow()
    if console_hwnd:
        win32gui.ShowWindow(console_hwnd, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(console_hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(console_hwnd)

# Add known game process names or window titles here
KNOWN_GAMES = ['eldenring.exe', 'dota2.exe', 'fortnite.exe']
CHECK_INTERVAL = 60  # seconds to wait before re-checking if gaming

def is_game_running():
    try:
        active_win = gw.getActiveWindow()
        if active_win and any(name.lower() in active_win.title.lower() for name in KNOWN_GAMES):
            return True
    except Exception:
        pass

    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() in KNOWN_GAMES:
            return True

    return False

def run_word_script(word_count=10):
    bring_self_to_front()
    subprocess.run(["python", "randomwords.py", "--count", str(word_count)])

def wait_random_interval(min_hours=1, max_hours=4):
    return random.randint(min_hours * 3600, max_hours * 3600)

def countdown(seconds):
    for remaining in range(seconds, 0, -1):
        if exit_event.is_set():
            print("\nExiting...")
            exit()
        if trigger_event.is_set():
            print("\n[Ctrl+]] Manual word generation triggered.")
            break

        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        secs = remaining % 60
        time_str = f"Next run in {hrs:02d}:{mins:02d}:{secs:02d}"
        print(f"\r{time_str}", end='', flush=True)
        time.sleep(1)
    print()

def key_listener():
    while True:
        if keyboard.is_pressed('ctrl+\\'):
            exit_event.set()
            break
        if keyboard.is_pressed('ctrl+]'):
            trigger_event.set()
        time.sleep(0.1)

# Start keyboard listener in the background
threading.Thread(target=key_listener, daemon=True).start()

# Main loop
while True:
    os.system('cls')
    print("Launching word generator... Press Ctrl+] to trigger early, Ctrl+\\ to exit.")
    run_word_script(word_count=10)

    delay = wait_random_interval()
    countdown(delay)

    trigger_event.clear()

    while is_game_running():
        print("Game detected. Pausing...")
        time.sleep(CHECK_INTERVAL)
