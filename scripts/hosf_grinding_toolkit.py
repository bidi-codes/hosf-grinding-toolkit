"""
Heroes of Science and Fiction - Achievement Grinding Toolkit
A collection of automation scripts to help with the toughest achievement grinds.
All scripts can be stopped with ESC at any time.

Requirements: pip install pyautogui pynput
To compile to .exe: pip install pyinstaller && pyinstaller --onefile --windowed hosf_toolkit.py
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import pyautogui
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener, Button


# ============================================================
# GLOBAL STATE
# ============================================================
active_thread = None
stop_event = threading.Event()
keyboard_ctrl = KeyboardController()
global_keyboard_listener = None


def is_running():
    return active_thread is not None and active_thread.is_alive()


def request_stop():
    stop_event.set()


# ============================================================
# HELPER: create labeled input field
# ============================================================
def make_field(parent, label, default, row, help_text="", width=12):
    frame = tk.Frame(parent, bg="#1e1e2e")

    lbl = tk.Label(frame, text=label, font=("Consolas", 10), fg="#cdd6f4", bg="#1e1e2e", anchor="w")
    lbl.pack(side="left", padx=(0, 8))

    entry = tk.Entry(frame, width=width, font=("Consolas", 10), bg="#313244", fg="#cdd6f4",
                     insertbackground="#cdd6f4", relief="flat", bd=0, highlightthickness=1,
                     highlightcolor="#89b4fa", highlightbackground="#45475a")
    entry.insert(0, str(default))
    entry.pack(side="left", padx=(0, 8))

    if help_text:
        hint = tk.Label(frame, text=help_text, font=("Consolas", 9), fg="#6c7086", bg="#1e1e2e", anchor="w")
        hint.pack(side="left")

    frame.pack(fill="x", padx=16, pady=3)
    return entry


def make_section_label(parent, text):
    lbl = tk.Label(parent, text=text, font=("Consolas", 11, "bold"), fg="#89b4fa", bg="#1e1e2e", anchor="w")
    lbl.pack(fill="x", padx=16, pady=(12, 4))


def make_help_label(parent, text):
    lbl = tk.Label(parent, text=text, font=("Consolas", 9), fg="#a6adc8", bg="#1e1e2e",
                   anchor="w", justify="left", wraplength=700)
    lbl.pack(fill="x", padx=16, pady=(0, 4))


# ============================================================
# TAB: Mouse Capture
# ============================================================
def build_mouse_capture_tab(notebook):
    tab = tk.Frame(notebook, bg="#1e1e2e")
    notebook.add(tab, text=" 🖱 Mouse Capture ")

    make_section_label(tab, "Capture Mouse Positions")
    make_help_label(tab, "Click anywhere on screen to capture that position.\n"
                         "Positions are listed below. Use them as coordinates in other tabs.\n"
                         "Press ESC to stop capturing.")

    # Listbox for captured positions
    list_frame = tk.Frame(tab, bg="#1e1e2e")
    list_frame.pack(fill="both", expand=True, padx=16, pady=8)

    listbox = tk.Listbox(list_frame, font=("Consolas", 11), bg="#313244", fg="#cdd6f4",
                         selectbackground="#89b4fa", selectforeground="#1e1e2e",
                         relief="flat", bd=0, highlightthickness=1, highlightcolor="#89b4fa",
                         highlightbackground="#45475a", height=12)
    listbox.pack(fill="both", expand=True)

    # Buttons
    btn_frame = tk.Frame(tab, bg="#1e1e2e")
    btn_frame.pack(fill="x", padx=16, pady=(0, 8))

    status_var = tk.StringVar(value="Ready")
    mouse_listener_ref = [None]

    def start_capture():
        if is_running():
            status_var.set("⚠ Another script is running. Stop it first.")
            return

        listbox.delete(0, tk.END)
        stop_event.clear()
        status_var.set("Capturing... click anywhere. ESC to stop.")

        counter = [0]

        def on_click(x, y, button, pressed):
            if pressed and button == Button.left:
                counter[0] += 1
                text = f"#{counter[0]}:  x={x},  y={y}"
                listbox.insert(tk.END, text)
                listbox.see(tk.END)

        def on_key(key):
            if key == Key.esc:
                stop_event.set()
                if mouse_listener_ref[0]:
                    mouse_listener_ref[0].stop()
                status_var.set(f"Done. Captured {counter[0]} positions.")
                return False

        mouse_listener_ref[0] = MouseListener(on_click=on_click)
        mouse_listener_ref[0].start()

        kb_listener = KeyboardListener(on_press=on_key)
        kb_listener.start()

    def clear_list():
        listbox.delete(0, tk.END)
        status_var.set("Ready")

    start_btn = tk.Button(btn_frame, text="▶ Start Capture", font=("Consolas", 10, "bold"),
                          bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                          cursor="hand2", command=start_capture)
    start_btn.pack(side="left", padx=(0, 8))

    clear_btn = tk.Button(btn_frame, text="✕ Clear", font=("Consolas", 10),
                          bg="#f38ba8", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                          cursor="hand2", command=clear_list)
    clear_btn.pack(side="left")

    status_lbl = tk.Label(tab, textvariable=status_var, font=("Consolas", 10), fg="#a6adc8", bg="#1e1e2e")
    status_lbl.pack(fill="x", padx=16, pady=(0, 12))

    return tab


# ============================================================
# TAB: Auto End Turn
# ============================================================
def build_end_turn_tab(notebook):
    tab = tk.Frame(notebook, bg="#1e1e2e")
    notebook.add(tab, text=" 🔄 End Turn ")

    make_section_label(tab, "Auto End Turn")
    make_help_label(tab, "Presses E (end turn), then Enter twice (cycle + player confirmations).\n"
                         "Runs until you press ESC. Great for the 10 000 turns achievement \"One more turn\".\n"
                         "IMPORTANT: Make sure you go to OPTIONS in-game and disable \"Show dialog about available actions at the end of turn\".")

    make_section_label(tab, "Delays (seconds)")
    e_delay = make_field(tab, "After E press:", "0.1", 0, "delay after pressing E to end turn")
    c_delay = make_field(tab, "After cycle confirm:", "0.3", 1, "delay after first Enter (new cycle popup)")
    p_delay = make_field(tab, "After player confirm:", "0.1", 2, "delay after second Enter (player turn popup)")

    # Status and buttons
    status_var = tk.StringVar(value="Ready")

    def run_end_turn():
        global active_thread
        if is_running():
            status_var.set("⚠ Another script is running. Stop it first.")
            return

        stop_event.clear()

        try:
            d_e = float(e_delay.get())
            d_c = float(c_delay.get())
            d_p = float(p_delay.get())
        except ValueError:
            status_var.set("⚠ Invalid delay values. Please enter valid numbers.")
            return

        def loop():
            global active_thread
            status_var.set("Starting in 5 seconds... switch to game!")
            time.sleep(5)  # Initial delay to allow the user to switch to the game

            while not stop_event.is_set():
                # Press 'E' to end the turn
                keyboard_ctrl.press('e')
                keyboard_ctrl.release('e')
                time.sleep(d_e)

                # Press 'Enter' for cycle confirmation
                keyboard_ctrl.press(Key.enter)
                keyboard_ctrl.release(Key.enter)
                time.sleep(d_c)

                # Press 'Enter' for player confirmation
                keyboard_ctrl.press(Key.enter)
                keyboard_ctrl.release(Key.enter)
                time.sleep(d_p)

                # Display a generic running message
                status_var.set("Running... Press ESC to stop.")

        active_thread = threading.Thread(target=loop, daemon=True)
        active_thread.start()

    btn_frame = tk.Frame(tab, bg="#1e1e2e")
    btn_frame.pack(fill="x", padx=16, pady=12)

    start_btn = tk.Button(btn_frame, text="▶ Start", font=("Consolas", 10, "bold"),
                          bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                          cursor="hand2", command=run_end_turn)
    start_btn.pack(side="left", padx=(0, 8))

    stop_btn = tk.Button(btn_frame, text="⏹ Stop", font=("Consolas", 10, "bold"),
                         bg="#f38ba8", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                         cursor="hand2", command=request_stop)
    stop_btn.pack(side="left")

    status_lbl = tk.Label(tab, textvariable=status_var, font=("Consolas", 10), fg="#a6adc8", bg="#1e1e2e")
    status_lbl.pack(fill="x", padx=16, pady=(0, 12))

    return tab


# ============================================================
# TAB: Move (500k tiles grind)
# ============================================================
def build_move_tab(notebook):
    tab = tk.Frame(notebook, bg="#1e1e2e")
    notebook.add(tab, text=" 🚶 Move ")

    make_section_label(tab, "Auto Move (Left-Right)")
    make_help_label(tab, "Moves commander back and forth between two points.\n"
                         "For the 500 000 tiles achievement \"I will walk 500 000 tiles\". Restores movement after each trip.\n"
                         "Use Mouse Capture tab to find coordinates.")

    make_section_label(tab, "Click Positions")
    a_x = make_field(tab, "Point A  x:", "1500", 0, "right side; if drifting right, decrease")
    a_y = make_field(tab, "Point A  y:", "538", 1)
    b_x = make_field(tab, "Point B  x:", "440", 2, "left side; if drifting left, increase")
    b_y = make_field(tab, "Point B  y:", "538", 3)
    r_x = make_field(tab, "Restore  x:", "107", 4, "testtools refill movement button")
    r_y = make_field(tab, "Restore  y:", "15", 5)

    make_section_label(tab, "Timing")
    move_time = make_field(tab, "Move time:", "1", 6, "seconds to reach point (1 for 4x commander speed, 2.25 for normal speed)")
    restore_delay = make_field(tab, "Restore delay:", "0.1", 7, "seconds after clicking restore")

    status_var = tk.StringVar(value="Ready")

    def run_move():
        global active_thread
        if is_running():
            status_var.set("⚠ Another script is running. Stop it first.")
            return

        stop_event.clear()
        A = (int(a_x.get()), int(a_y.get()))
        B = (int(b_x.get()), int(b_y.get()))
        RESTORE = (int(r_x.get()), int(r_y.get()))
        mt = float(move_time.get())
        rd = float(restore_delay.get())

        def loop():
            global active_thread
            status_var.set("Starting in 5 seconds... switch to game!")
            time.sleep(5)
            TILES_PER_TRIP = 12  # each A<->B trip covers approximately 12 tiles
            trips = 0
            while not stop_event.is_set():
                pyautogui.click(A)
                pyautogui.press('m')
                time.sleep(mt)
                pyautogui.click(RESTORE)
                time.sleep(rd)

                pyautogui.click(B)
                pyautogui.press('m')
                time.sleep(mt)
                pyautogui.click(RESTORE)
                time.sleep(rd)

                trips += 2
                if trips % 2 == 0:
                    status_var.set(f"Running... Trips: {trips} | ~{trips * TILES_PER_TRIP} tiles")
            status_var.set(f"Stopped after {trips} trips (~{trips * TILES_PER_TRIP} tiles).")
            active_thread = None

        active_thread = threading.Thread(target=loop, daemon=True)
        active_thread.start()

    btn_frame = tk.Frame(tab, bg="#1e1e2e")
    btn_frame.pack(fill="x", padx=16, pady=12)

    start_btn = tk.Button(btn_frame, text="▶ Start", font=("Consolas", 10, "bold"),
                          bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                          cursor="hand2", command=run_move)
    start_btn.pack(side="left", padx=(0, 8))

    stop_btn = tk.Button(btn_frame, text="⏹ Stop", font=("Consolas", 10, "bold"),
                         bg="#f38ba8", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                         cursor="hand2", command=request_stop)
    stop_btn.pack(side="left")

    status_lbl = tk.Label(tab, textvariable=status_var, font=("Consolas", 10), fg="#a6adc8", bg="#1e1e2e")
    status_lbl.pack(fill="x", padx=16, pady=(0, 12))

    return tab


# ============================================================
# TAB: Collect (15k items grind)
# ============================================================
def build_collect_tab(notebook):
    tab = tk.Frame(notebook, bg="#1e1e2e")
    notebook.add(tab, text=" 📦 Collect ")

    # Scrollable frame
    canvas = tk.Canvas(tab, bg="#1e1e2e", highlightthickness=0)
    scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#1e1e2e")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mouse wheel scrolling
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    make_section_label(scroll_frame, "Auto Collect (Snake Pattern)")
    make_help_label(scroll_frame, "Traverses the map in a snake pattern collecting items tile by tile.\n"
                                  "For the 15 000 collectibles \"Hoarder\" and 5 000 sell \"Yard sale\" achievements.\n"
                                  "Place commander in bottom-left corner of a map filled with items.\n"
                                  "Uses click + M + click + M per tile to collect and move.")

    make_section_label(scroll_frame, "Tile Positions (relative to commander)")
    l_x = make_field(scroll_frame, "Left tile  x:", "1020", 0, "if clicking on commander, increase x")
    l_y = make_field(scroll_frame, "Left tile  y:", "540", 1)
    r_x = make_field(scroll_frame, "Right tile x:", "900", 2, "if clicking on commander, decrease x")
    r_y = make_field(scroll_frame, "Right tile y:", "540", 3)
    u_x = make_field(scroll_frame, "Up tile    x:", "963", 4)
    u_y = make_field(scroll_frame, "Up tile    y:", "507", 5)
    re_x = make_field(scroll_frame, "Restore    x:", "107", 6, "testtools refill movement button")
    re_y = make_field(scroll_frame, "Restore    y:", "15", 7)

    make_section_label(scroll_frame, "Map Size")
    line_f = make_field(scroll_frame, "Tiles per row:", "39", 8, "width - 1 (commander occupies one tile)")
    rows_f = make_field(scroll_frame, "Rows:", "39", 9, "height - 1")

    make_section_label(scroll_frame, "Timing (seconds)")
    dwl = make_field(scroll_frame, "Walk delay (row):", "0.25", 10, "wait after moving one tile on a row")
    dwc = make_field(scroll_frame, "Walk delay (up):", "0.75", 11, "wait after moving one tile up")
    dac = make_field(scroll_frame, "After click:", "0.05", 12, "wait after clicking a tile before M")
    dam = make_field(scroll_frame, "After M:", "0.1", 13, "wait after pressing M before second click")
    dar = make_field(scroll_frame, "After restore:", "0.1", 14, "wait after clicking restore")

    make_section_label(scroll_frame, "Restore Frequency")
    rev = make_field(scroll_frame, "Restore every:", "30", 15, "tiles between restore clicks (based on movement points)")

    status_var = tk.StringVar(value="Ready")

    def run_collect():
        global active_thread
        if is_running():
            status_var.set("⚠ Another script is running. Stop it first.")
            return

        stop_event.clear()
        LEFT = (int(l_x.get()), int(l_y.get()))
        RIGHT = (int(r_x.get()), int(r_y.get()))
        UP = (int(u_x.get()), int(u_y.get()))
        RESTORE = (int(re_x.get()), int(re_y.get()))
        LINE = int(line_f.get())
        ROWS = int(rows_f.get())
        DELAY_WALK_LINE = float(dwl.get())
        DELAY_WALK_COLUMN = float(dwc.get())
        DELAY_AFTER_CLICK = float(dac.get())
        DELAY_AFTER_M = float(dam.get())
        DELAY_AFTER_RESTORE = float(dar.get())
        RESTORE_EVERY = int(rev.get())

        def loop():
            global active_thread
            status_var.set("Starting in 5 seconds... switch to game!")
            time.sleep(5)
            collected = 0

            for row in range(ROWS):
                if stop_event.is_set():
                    break
                coords = LEFT if row % 2 == 0 else RIGHT
                direction = "LEFT" if row % 2 == 0 else "RIGHT"

                for col in range(LINE):
                    if stop_event.is_set():
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
                        time.sleep(DELAY_AFTER_RESTORE)

                    if collected % 10 == 0:
                        status_var.set(f"Running... Row {row + 1}/{ROWS} going {direction} | Collected: ~{collected}")

                if not stop_event.is_set():
                    pyautogui.click(RESTORE)
                    time.sleep(DELAY_AFTER_RESTORE)

                if row < ROWS - 1 and not stop_event.is_set():
                    pyautogui.click(UP)
                    time.sleep(DELAY_AFTER_CLICK)
                    pyautogui.press('m')
                    time.sleep(DELAY_AFTER_M)
                    pyautogui.click(UP)
                    time.sleep(DELAY_AFTER_CLICK)
                    pyautogui.press('m')
                    time.sleep(DELAY_WALK_COLUMN)

            status_var.set(f"Done! Collected approximately {collected} items.")
            active_thread = None

        active_thread = threading.Thread(target=loop, daemon=True)
        active_thread.start()

    btn_frame = tk.Frame(scroll_frame, bg="#1e1e2e")
    btn_frame.pack(fill="x", padx=16, pady=12)

    start_btn = tk.Button(btn_frame, text="▶ Start", font=("Consolas", 10, "bold"),
                          bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                          cursor="hand2", command=run_collect)
    start_btn.pack(side="left", padx=(0, 8))

    stop_btn = tk.Button(btn_frame, text="⏹ Stop", font=("Consolas", 10, "bold"),
                         bg="#f38ba8", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                         cursor="hand2", command=request_stop)
    stop_btn.pack(side="left")

    status_lbl = tk.Label(scroll_frame, textvariable=status_var, font=("Consolas", 10), fg="#a6adc8", bg="#1e1e2e")
    status_lbl.pack(fill="x", padx=16, pady=(0, 12))

    return tab


# ============================================================
# TAB: Sell
# ============================================================
def build_sell_tab(notebook):
    tab = tk.Frame(notebook, bg="#1e1e2e")
    notebook.add(tab, text=" 💰 Sell ")

    make_section_label(tab, "Auto Sell")
    make_help_label(tab, "Clicks the Sell button repeatedly.\n"
                         "For the 5 000 items sold achievement \"Yard sale\".\n"
                         "Open a Black Market or Traveling Merchant first, then start.")

    make_section_label(tab, "Button Position")
    s_x = make_field(tab, "Sell button x:", "1244", 0, "use Mouse Capture to find position")
    s_y = make_field(tab, "Sell button y:", "513", 1)

    make_section_label(tab, "Timing")
    delay = make_field(tab, "Delay after sell:", "0.1", 2, "seconds between each sell click")

    status_var = tk.StringVar(value="Ready")

    def run_sell():
        global active_thread
        if is_running():
            status_var.set("⚠ Another script is running. Stop it first.")
            return

        stop_event.clear()
        SELL = (int(s_x.get()), int(s_y.get()))
        d = float(delay.get())

        def loop():
            global active_thread
            status_var.set("Starting in 5 seconds... switch to game!")
            time.sleep(5)
            sold = 0
            while not stop_event.is_set():
                pyautogui.click(SELL)
                time.sleep(d)
                sold += 1
                if sold % 100 == 0:
                    status_var.set(f"Running... Sold: {sold}")
            status_var.set(f"Stopped after {sold} sells.")
            active_thread = None

        active_thread = threading.Thread(target=loop, daemon=True)
        active_thread.start()

    btn_frame = tk.Frame(tab, bg="#1e1e2e")
    btn_frame.pack(fill="x", padx=16, pady=12)

    start_btn = tk.Button(btn_frame, text="▶ Start", font=("Consolas", 10, "bold"),
                          bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                          cursor="hand2", command=run_sell)
    start_btn.pack(side="left", padx=(0, 8))

    stop_btn = tk.Button(btn_frame, text="⏹ Stop", font=("Consolas", 10, "bold"),
                         bg="#f38ba8", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                         cursor="hand2", command=request_stop)
    stop_btn.pack(side="left")

    status_lbl = tk.Label(tab, textvariable=status_var, font=("Consolas", 10), fg="#a6adc8", bg="#1e1e2e")
    status_lbl.pack(fill="x", padx=16, pady=(0, 12))

    return tab


# ============================================================
# TAB: Town Portal
# ============================================================
def build_town_portal_tab(notebook):
    tab = tk.Frame(notebook, bg="#1e1e2e")
    notebook.add(tab, text=" 🌀 Town Portal ")

    make_section_label(tab, "Auto Town Portal")
    make_help_label(tab, "Presses G (teleport beam), clicks town from list, clicks Travel.\n"
                         "For the 500 town portal uses achievement \"Instant visit\".\n"
                         "You need at least 2 towns. Stay inside a town.")

    make_section_label(tab, "Click Positions")
    t_x = make_field(tab, "Town select x:", "829", 0, "first town in the teleport list")
    t_y = make_field(tab, "Town select y:", "435", 1)
    tr_x = make_field(tab, "Travel btn  x:", "831", 2, "Travel button position")
    tr_y = make_field(tab, "Travel btn  y:", "679", 3)

    make_section_label(tab, "Timing (seconds)")
    dg = make_field(tab, "After G press:", "0.1", 4, "wait for teleport beam menu to open")
    dt = make_field(tab, "After town select:", "0.1", 5, "wait after clicking town in list")
    dtr = make_field(tab, "After Travel:", "0.5", 6, "wait for teleport animation to finish")

    status_var = tk.StringVar(value="Ready")

    def run_portal():
        global active_thread
        if is_running():
            status_var.set("⚠ Another script is running. Stop it first.")
            return

        stop_event.clear()
        TOWN = (int(t_x.get()), int(t_y.get()))
        TRAVEL = (int(tr_x.get()), int(tr_y.get()))
        d_g = float(dg.get())
        d_t = float(dt.get())
        d_tr = float(dtr.get())

        def loop():
            global active_thread
            status_var.set("Starting in 5 seconds... switch to game!")
            time.sleep(5)
            teleports = 0
            while not stop_event.is_set():
                keyboard_ctrl.press('g')
                keyboard_ctrl.release('g')
                time.sleep(d_g)
                pyautogui.click(TOWN)
                time.sleep(d_t)
                pyautogui.click(TRAVEL)
                time.sleep(d_tr)
                teleports += 1
                if teleports % 10 == 0:
                    status_var.set(f"Running... Teleports: {teleports}")
            status_var.set(f"Stopped after {teleports} teleports.")
            active_thread = None

        active_thread = threading.Thread(target=loop, daemon=True)
        active_thread.start()

    btn_frame = tk.Frame(tab, bg="#1e1e2e")
    btn_frame.pack(fill="x", padx=16, pady=12)

    start_btn = tk.Button(btn_frame, text="▶ Start", font=("Consolas", 10, "bold"),
                          bg="#a6e3a1", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                          cursor="hand2", command=run_portal)
    start_btn.pack(side="left", padx=(0, 8))

    stop_btn = tk.Button(btn_frame, text="⏹ Stop", font=("Consolas", 10, "bold"),
                         bg="#f38ba8", fg="#1e1e2e", relief="flat", padx=16, pady=6,
                         cursor="hand2", command=request_stop)
    stop_btn.pack(side="left")

    status_lbl = tk.Label(tab, textvariable=status_var, font=("Consolas", 10), fg="#a6adc8", bg="#1e1e2e")
    status_lbl.pack(fill="x", padx=16, pady=(0, 12))

    return tab


# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    root = tk.Tk()
    root.title("Heroes of Science and Fiction - Achievement Grinding Toolkit")
    root.geometry("820x640")
    root.configure(bg="#1e1e2e")
    root.resizable(True, True)

    # Title bar
    title_frame = tk.Frame(root, bg="#181825", pady=8)
    title_frame.pack(fill="x")

    title_lbl = tk.Label(title_frame,
                         text="⚔ HoSF Achievement Grinding Toolkit",
                         font=("Consolas", 14, "bold"), fg="#cba6f7", bg="#181825")
    title_lbl.pack(side="left", padx=16)

    # Screen resolution display
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    res_lbl = tk.Label(title_frame,
                       text=f"Screen: {screen_w}x{screen_h}",
                       font=("Consolas", 10), fg="#6c7086", bg="#181825")
    res_lbl.pack(side="right", padx=16)

    # ESC info
    esc_lbl = tk.Label(title_frame,
                       text="ESC stops any running script",
                       font=("Consolas", 9), fg="#f38ba8", bg="#181825")
    esc_lbl.pack(side="right", padx=16)

    # Style for notebook tabs
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
    style.configure("TNotebook.Tab", background="#313244", foreground="#cdd6f4",
                    font=("Consolas", 10), padding=[12, 6])
    style.map("TNotebook.Tab",
              background=[("selected", "#45475a")],
              foreground=[("selected", "#cba6f7")])

    # Notebook (tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=4, pady=4)

    build_mouse_capture_tab(notebook)
    build_end_turn_tab(notebook)
    build_move_tab(notebook)
    build_collect_tab(notebook)
    build_sell_tab(notebook)
    build_town_portal_tab(notebook)

    # Global ESC listener
    def global_esc(key):
        if key == Key.esc:
            request_stop()

    global global_keyboard_listener
    global_keyboard_listener = KeyboardListener(on_press=global_esc)
    global_keyboard_listener.start()

    # Clean shutdown
    def on_close():
        request_stop()
        if global_keyboard_listener:
            global_keyboard_listener.stop()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()


if __name__ == "__main__":
    main()