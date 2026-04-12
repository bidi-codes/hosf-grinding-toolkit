import time
import threading
import pyautogui
from pynput.keyboard import Key, Listener

# --- PARAMETERS ---
SELL_BUTTON = (1244, 513)  # position of the Sell button
DELAY_AFTER_SELL = 0.1  # delay after each sell click
# ------------------

stop_flag = threading.Event()

def on_press(key):
    if key == Key.esc:
        stop_flag.set()
        return False

listener = Listener(on_press=on_press)
listener.start()

print("Starting in 5 seconds... press ESC to stop. Switch to the game window!")
time.sleep(5)

sold = 0
while not stop_flag.is_set():
    pyautogui.click(SELL_BUTTON)
    time.sleep(DELAY_AFTER_SELL)
    sold += 1
    if sold % 500 == 0:
        print(f"Sold: {sold}")

print(f"Stopped after {sold} sells.")