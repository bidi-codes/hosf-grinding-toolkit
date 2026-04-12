import time
import pyautogui
from pynput import keyboard

running = True

def on_press(key):
    global running
    if key == keyboard.Key.esc:
        running = False

listener = keyboard.Listener(on_press=on_press)
listener.start()

# --- PARAMETERS ---
A = (1500, 538)  # right click point; if drifting right, decrease x (e.g. 1480, 1460...)
B = (440, 538)   # left click point; if drifting left, increase x (e.g. 460, 480...)
RESTORE = (107, 15)  # testtools refill movement button position
MOVE_TIME = 1  # how long it takes to reach the point; adjust as needed
# 2.25 for normal speed game
# 1 with quadrupled speed obtained through regedit
DELAY_AFTER_RESTORE = 0.1  # delay after clicking restore
# ------------------

print("Starting in 5 seconds... press ESC to stop. Switch to the game window!")
time.sleep(5)

steps = 0
while running:
    pyautogui.click(A)
    pyautogui.press('m')
    time.sleep(MOVE_TIME)
    pyautogui.click(RESTORE)
    time.sleep(DELAY_AFTER_RESTORE)

    pyautogui.click(B)
    pyautogui.press('m')
    time.sleep(MOVE_TIME)
    pyautogui.click(RESTORE)
    time.sleep(DELAY_AFTER_RESTORE)

    steps += 2
    if steps % 100 == 0:
        print(f"Steps: {steps}")

print(f"Stopped after {steps} steps.")