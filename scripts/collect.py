import time
import pyautogui
from pynput.keyboard import Key, Listener

stop_flag = False

def on_press(key):
    global stop_flag
    if key == Key.esc:
        stop_flag = True
        return False

listener = Listener(on_press=on_press)
listener.start()

# --- PARAMETERS ---
LEFT = (1020, 540)   # one tile to the left; if clicking on commander, increase x (e.g. 1040, 1060...)
RIGHT = (900, 540)   # one tile to the right; if clicking on commander, decrease x (e.g. 880, 860...)
UP = (963, 507)      # one tile up
RESTORE = (107, 15)  # testtools refill movement button position

LINE = 39   # how many tiles to collect per row
ROWS = 39   # how many rows to traverse

DELAY_WALK_LINE = 0.25     # delay after moving one tile on a row (wait for walk animation)
DELAY_WALK_COLUMN = 0.75   # delay after moving one tile up (wait for walk animation)
DELAY_AFTER_CLICK = 0.05   # delay after clicking a tile (before pressing M)
DELAY_AFTER_M = 0.1        # delay after pressing M (before second click+M to collect)
DELAY_AFTER_RESTORE = 0.1  # delay after clicking restore

RESTORE_EVERY = 30  # restore movement points every N tiles
# ------------------

print("Starting in 5 seconds... press ESC to stop. Switch to the game window!")
time.sleep(5)

collected = 0
for row in range(ROWS):
    if stop_flag:
        break
    direction = "LEFT" if row % 2 == 0 else "RIGHT"
    coords = LEFT if row % 2 == 0 else RIGHT
    print(f"--- Row {row + 1}/{ROWS} going {direction} ---")

    for col in range(LINE):
        if stop_flag:
            break
        pyautogui.click(coords)
        time.sleep(DELAY_AFTER_CLICK)
        pyautogui.press('m')
        time.sleep(DELAY_AFTER_M)
        pyautogui.click(coords)
        time.sleep(DELAY_AFTER_CLICK)
        pyautogui.press('m')
        time.sleep(DELAY_WALK_LINE)
        collected += 1
        if (col + 1) % RESTORE_EVERY == 0:
            pyautogui.click(RESTORE)
            print(f"  Tile {col + 1}/{LINE} - RESTORED | Total: {collected}")
            time.sleep(DELAY_AFTER_RESTORE)
        else:
            print(f"  Tile {col + 1}/{LINE}")

    if not stop_flag:
        pyautogui.click(RESTORE)
        print(f"  End of row restore | Total: {collected}")
        time.sleep(DELAY_AFTER_RESTORE)

    if row < ROWS - 1 and not stop_flag:
        pyautogui.click(UP)
        time.sleep(DELAY_AFTER_CLICK)
        pyautogui.press('m')
        time.sleep(DELAY_AFTER_M)
        pyautogui.click(UP)
        time.sleep(DELAY_AFTER_CLICK)
        pyautogui.press('m')
        print(f"  Moving UP")
        time.sleep(DELAY_WALK_COLUMN)

print(f"Done! Collected approximately {collected} items.")