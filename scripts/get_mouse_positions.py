import time
import pyautogui
from pynput import mouse, keyboard

stop_flag = False
positions = []

def on_click(x, y, button, pressed):
    if pressed and button == mouse.Button.left:
        positions.append((x, y))
        print(f"#{len(positions)}: x={x}, y={y}")

def on_press(key):
    global stop_flag
    if key == keyboard.Key.esc:
        stop_flag = True
        return False

print("Starting in 3 seconds... switch to the game window!")
time.sleep(3)
print("Click anywhere to capture position. Press ESC to stop.")
print("---")

mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener.start()
keyboard_listener.start()
keyboard_listener.join()
mouse_listener.stop()

print("---")
print(f"Captured {len(positions)} positions:")
for i, pos in enumerate(positions, 1):
    print(f"  #{i}: x={pos[0]}, y={pos[1]}")