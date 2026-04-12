import time
import threading
from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()

# --- PARAMETERS ---
DELAY_AFTER_END_TURN = 0.1    # delay after pressing E (end turn)
DELAY_AFTER_CYCLE_CONFIRM = 0.3  # delay after first Enter (cycle confirmation)
DELAY_AFTER_PLAYER_CONFIRM = 0.1  # delay after second Enter (player turn confirmation)
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

turn = 0
while not stop_flag.is_set():
    turn += 1
    keyboard.press('e')
    keyboard.release('e')
    time.sleep(DELAY_AFTER_END_TURN)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(DELAY_AFTER_CYCLE_CONFIRM)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(DELAY_AFTER_PLAYER_CONFIRM)
    if turn % 100 == 0:
        print(f"Turn {turn}")

print(f"Stopped after {turn} turns.")