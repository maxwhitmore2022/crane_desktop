# Tower Crane Challenge

Tower Crane Challenge is a Python desktop game. You control a tower crane, pick up two loads from a staging area, and place them at marked locations before the timer runs out. The game displays a load chart and warns you if the suspended load approaches the allowed capacity.

The game runs in a desktop window. You do not need to open `index.html`, run a web server, or use a browser to play the Python version.

## What you need

- A computer with a graphical desktop, a keyboard, and a mouse or trackpad. Tkinter needs access to a display; an ordinary terminal-only or headless session cannot open the game window.
- **Python 3.10 or newer.** The game uses Python features introduced in Python 3.10. Python 3.15 was available in the environment used for development; other versions and operating systems have not all been verified.
- **Tkinter**, Python's desktop interface library, with Tcl/Tk installed. Tkinter is part of Python's standard library, but some Python installations or Linux distributions package it separately.
- **Matplotlib**, installed into the Python environment used to run the game. It draws the crane scene and load chart inside the Tkinter window.
- **NumPy** is a Matplotlib dependency and is also named in the project specification. Matplotlib normally installs it automatically; the installation commands below request it explicitly. The current application code does not import NumPy directly.
- **pip**, Python's package installer, to install the Python packages.

The game also uses `math`, `time`, `random`, `dataclasses`, and `bisect` from Python's standard library. These do not need separate pip installations.

## 1. Open a terminal in the project folder

The project folder is the folder containing `app.py`, `crane_scene.py`, `game_state.py`, and `crane_calculations.py`. Open a terminal and change into that folder. Quote the path if it contains spaces:

```sh
cd "/path/to/crane_desktop"
```

On Windows, use your actual folder path instead:

```powershell
cd "C:\path\to\crane_desktop"
```

Run the commands in the following sections from this folder. Leave the terminal open while the game is running so you can see any error messages.

## 2. Check Python and Tkinter

### macOS and Linux

```sh
python3 --version
python3 -m pip --version
python3 -m tkinter
```

### Windows PowerShell

```powershell
py --version
py -m pip --version
py -m tkinter
```

`python3 -m tkinter` or `py -m tkinter` should open a small Tkinter window. Close that window to return to the terminal. If it does not open, resolve the Tkinter installation before running the game; installing Matplotlib alone will not provide Tkinter.

On some Windows installations, `py` may be unavailable even though `python` works. In that case use `python` in place of `py` in the Windows commands. On macOS or Linux, if your installation uses `python` for Python 3, you may use it in place of `python3`. Check the version first.

## 3. Create a virtual environment

A virtual environment keeps this project's installed packages separate from other Python projects. It is recommended, though not required.

### macOS and Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

After activation, the shell typically displays `(.venv)` in its prompt. The commands below use `python` to refer to the interpreter in the active environment. Activate the environment again whenever you open a new terminal to work on the game.

If PowerShell prevents the activation script from running, you can use the environment's Python directly without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install matplotlib numpy
.\.venv\Scripts\python.exe app.py
```

If you choose not to use a virtual environment, use the same Python interpreter for both installation and launch: for example, `python3 -m pip` followed by `python3 app.py`, or `py -m pip` followed by `py app.py`.

## 4. Install the packages

With the virtual environment active, run:

```sh
python -m pip install matplotlib numpy
```

This installs Matplotlib and NumPy into the active environment. `python -m pip` is useful because it installs packages for the same interpreter that `python` starts. An internet connection is normally needed to download packages during installation.

Check that the interpreter can import the required libraries:

```sh
python -c "import tkinter, matplotlib, numpy; print('Tkinter:', tkinter.TkVersion, 'Matplotlib:', matplotlib.__version__, 'NumPy:', numpy.__version__)"
```

The command prints versions if all three imports succeed. The separate `python -m tkinter` window check above is still useful because a successful import alone does not prove a graphical window can open.

There is currently no `requirements.txt` or `pyproject.toml` in this project, and package versions are not pinned. Installation may select different compatible package versions on different Python versions or platforms.

## 5. Start the game

With the virtual environment active and the terminal in the project folder:

```sh
python app.py
```

A **Tower Crane Challenge** window and a **How to play** dialog should appear. Close the dialog, then press **Start Level** to start the timer. To exit, close the game window. If you activated a virtual environment, you can leave it after closing the game by running:

```sh
deactivate
```

## How to play

1. Each level starts with two randomly selected loads. The four available weights are 4,000, 6,000, 8,000, and 10,000 lb. Before starting, use the load buttons to change the selection if you wish; exactly two loads must be selected. Deselect a selected load before selecting a replacement.
2. Press **Start Level**. The level has a three-minute timer.
3. Move the trolley over the staging conveyor and lower the hook, then press **Enter** to pick up the next selected load. The game picks the next available selected load in the displayed list.
4. Move the load toward an unfilled target. The target label shows its required jib angle. Hold **Left Arrow** to make the angle more negative or **Right Arrow** to make it more positive. Target A requires approximately −34°; target B requires approximately +34°. The angle guide below the scene shows the current angle and both target angles.
5. When the load is positioned within the target and the angle is close enough, the target lights up and shows **DROP!**; the guidance also says to press Enter. Press **Enter** to deliver. An invalid drop returns the load to staging.
6. Deliver both loads to complete the level. Press **Continue / Next Level** to move on, or **Retry Level** to reset the current level. A retry removes points earned on that level and restores its selected loads and timer.

### Controls

| Input | Action |
|---|---|
| **A** / **D** | Move the trolley left / right. |
| **W** / **S** | Raise / lower the hook. |
| **Left Arrow** / **Right Arrow** | Decrease / increase the jib swing angle. Hold the key to keep swinging. |
| **Enter** | Pick up a load at staging, or attempt to drop a carried load. |
| **Crane color** button | Choose a color for the player crane. |
| **Dark mode** / **Light mode** button | Switch the scene theme. |
| **Retry Level** button | Reset the current level. |
| **Continue / Next Level** button | Advance after successfully completing a level. |

If keys do not seem to respond, click the game window so it has keyboard focus. Movement is active after starting a level. Close any open dialog before using the controls.

### Load chart and scoring

The right side of the window shows the load chart. Its highlighted row is the capacity used for the current radius. The game uses the capacity at the **next larger listed radius** when the radius falls between rows; for example, 62 ft uses the 75 ft capacity of 13,000 lb.

| Radius (ft) | Capacity (lb) |
|---:|---:|
| 50 | 20,000 |
| 75 | 13,000 |
| 100 | 9,000 |
| 125 | 7,000 |
| 150 | 5,500 |

A suspended load at or above 90% of the selected capacity is in caution. At or above 100%, the app displays an overload warning and resets the level. Each delivered pound earns one point. The radius is limited to 50–150 ft.

The current implementation uses the trolley-radius value for the chart; the visible horizontal position of the hook or load can differ because of jib swing and wind. The validation results and this known discrepancy are documented in `spec.md`. The load chart is a fictional game example, not a source of real crane lifting instructions.

## Troubleshooting

### `python` or `python3` is not found

Install Python 3.10 or newer, then open a new terminal. On Windows, try the Python launcher `py`. On macOS and Linux, try `python3`. Make sure the command you choose reports the intended Python version.

### `No module named tkinter` or `No module named _tkinter`

Your Python installation does not have a working Tkinter/Tcl/Tk setup. Install a Python distribution that includes Tkinter, or install your operating system's Tkinter package for the same Python version. On Debian/Ubuntu systems, the distribution package is commonly called `python3-tk`; use the package manager for your distribution and Python installation. Then repeat the Tkinter window check. A virtual environment uses the underlying Python installation's Tkinter support.

### `No module named matplotlib` or `No module named numpy`

Activate the virtual environment and rerun `python -m pip install matplotlib numpy`. Check `python --version` and `python -m pip --version` in the same terminal. If packages were installed with a different Python interpreter, install them with the interpreter you use to launch the game.

### The window does not open or an error mentions a display

Run the game from a desktop session with access to a graphical display. Remote or headless terminals may not have one. Run `python -m tkinter` first to check whether that interpreter can open a Tkinter window.

### Matplotlib reports that its configuration directory is not writable

Matplotlib may use a temporary cache and continue. If startup is slow or the warning persists, choose a writable directory for its configuration and cache. For example, in a macOS or Linux terminal:

```sh
mkdir -p /tmp/crane-matplotlib
MPLCONFIGDIR=/tmp/crane-matplotlib python app.py
```

In PowerShell, set `MPLCONFIGDIR` to a writable directory for that terminal session before starting the app.

### The game opens but I cannot deliver a load

Start the level, pick up a load, and check both the load position and the jib angle. Target A and target B require different angles, even when their positions appear close in the side view. Watch the separate angle guide and the target highlight; press Enter when the game says **READY TO DROP**. Wind moves the suspended load, so wait for it to enter the target if necessary.

## Project files

| File | Purpose |
|---|---|
| `app.py` | Creates the Tkinter window, connects controls, and runs the game update loop. |
| `crane_scene.py` | Draws the crane, targets, building, and load table using Matplotlib inside Tkinter. |
| `game_state.py` | Holds the level, loads, score, timer, target, and delivery rules. |
| `crane_calculations.py` | Holds the radius limits, load chart lookup, warning, and overload calculations. |
| `spec.md` | Describes the intended game behavior and records radius validation results. |
| `prompts.md` | Records project requests, changes, and their results. |
| `index.html` | Existing separate HTML artifact; it is not needed to start the Python desktop app. |
