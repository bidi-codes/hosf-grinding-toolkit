Download the latest toolkit [here](https://github.com/bidi-codes/hosf-grinding-toolkit/releases/tag/v1.0). Extract the zip and double-click hosf_grinding_toolkit.exe.

---

# Heroes of Science and Fiction - Achievement Grinding Toolkit

A collection of automation tools to help with the toughest
achievement grinds in Heroes of Science and Fiction.

---

## HOW TO USE

### Option 1: App (recommended, no setup needed)

1. Open the "app" folder
2. Double-click hosf_grinding_toolkit.exe
3. Pick a tab, set your coordinates, press Start
4. Press ESC at any time to stop

### Option 2: Python scripts (if you want to tweak the code)

1. Install Python from python.org (check "Add to PATH")
2. Open a terminal and run:

   ```
   pip install pyautogui pynput
   ```
3. Open the "scripts" folder
4. Edit parameters inside the script you need
5. Run with:

   ```
   python script_name.py
   ```
6. Press ESC at any time to stop

---

## IMPORTANT NOTES

* Coordinates depend on your screen resolution and game window.
  Use the Mouse Capture tab (or get_mouse_positions.py) to find
  the correct positions on YOUR screen.

* For faster movement animations, you can quadruple hero speed
  through the Windows Registry:

  1. Open regedit (Win+R, type regedit, Enter)
  2. Navigate to:

     ```
     HKEY_CURRENT_USER\SOFTWARE\Oxymoron Games\Silence of the Siren
     ```
  3. Find OPTION_EXPLORATION_ANIMATION_SPEED
  4. Double-click it and change "10 40" to "30 40" (quadruple speed)
  5. Restart the game

* All scripts are single-player automation only.
  No online, no multiplayer, nothing bannable.

* The -testools launch option (add in Steam game properties)
  enables dev buttons: instant kill in combat, refill movement,
  grant resources. Very useful for many achievements.

---

## TOOLS INCLUDED

* Mouse Capture    Find screen coordinates by clicking
* End Turn         Auto end turn (10,000 turns achievement)
* Move             Auto left-right movement (500,000 tiles achievement)
* Collect          Snake pattern item collection (15,000 items achievement)
* Sell             Auto sell at markets (5,000 sells achievement)
* Town Portal      Auto teleport between towns (500 portals achievement)

---

## TROUBLESHOOTING

* "It clicks in the wrong spot"
  Your resolution is different. Use Mouse Capture to find new coordinates.

* "Commander drifts to one side" (Move script)
  Adjust Point A or Point B. Comments in the fields explain which way.

* "Script runs too fast / too slow"
  Adjust the delay values. Start with higher values and decrease.

* "Exe won't start" / antivirus blocks it
  PyInstaller exes sometimes trigger false positives.
  Add an exception or use the Python scripts directly.

---

Made with love and way too many clicks. Enjoy! :D
