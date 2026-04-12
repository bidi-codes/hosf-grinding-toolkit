import time
import threading
import pyautogui
from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()

# --- PARAMETERS ---
TOWN_SELECT = (829, 435)  # position of the first town in the list
TRAVEL_BUTTON = (831, 679)  # position of the Travel button
DELAY_AFTER_G = 0.1  # delay after pressing G (opens teleport beam menu)
DELAY_AFTER_TOWN_SELECT = 0.1  # delay after clicking on town
DELAY_AFTER_TRAVEL = 0.5  # delay after clicking Travel (wait for teleport animation)
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

teleports = 0
while not stop_flag.is_set():
    keyboard.press('g')
    keyboard.release('g')
    time.sleep(DELAY_AFTER_G)
    pyautogui.click(TOWN_SELECT)
    time.sleep(DELAY_AFTER_TOWN_SELECT)
    pyautogui.click(TRAVEL_BUTTON)
    time.sleep(DELAY_AFTER_TRAVEL)
    teleports += 1
    if teleports % 50 == 0:
        print(f"Teleports: {teleports}")

print(f"Stopped after {teleports} teleports.")