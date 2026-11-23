# Crane Game
## Purpose
Players operate a tower crane in a side view, moving loads from a staging area to marked positions on a building under construction before a 3-minute timer expires. The goal is to complete deliveries without exceeding the crane load chart or tipping the crane.

## Inputs
### Keyboard controls
- **A:** move the trolley left on screen
- **D:** move the trolley right on screen
- **W:** raise the hook
- **S:** lower the hook
- **Left Arrow:** swing the jib left
- **Right Arrow:** swing the jib right
- **Enter:** pick up a load or set a carried load on a matching building position

The keyboard controls must remain visible on screen at all times during play, in a persistent control panel that is not hidden behind menus or overlays.

The crane has a tower, jib, trolley, cable, hook, and suspended-load indicator in a playful yellow construction setting.
The game also includes a computer-controlled second crane. The player must avoid collision between the crane components and suspended loads. The second crane follows a visible, predictable operating path.

## Calculations
The app calculates crane radius as the horizontal distance from the tower center to the suspended load or hook. A radius is compared against this example load chart:

| Radius (ft) | Capacity (lb) |
|---|---:|
| 50 | 20,000 |
| 75 | 13,000 |
| 100 | 9,000 |
| 125 | 7,000 |
| 150 | 5,500 |

For radii between table values, use the capacity at the next larger table radius. This is the conservative "round up" radius rule. For example, 62 ft uses the 75 ft capacity of 13,000 lb, and 138 ft uses the 150 ft capacity of 5,500 lb.

The capacity check uses the weight of the currently suspended load. The crane is not overweight below 100% of the allowed capacity. It warns exactly at 90% of capacity and tips at 100% or more.
The crane cannot operate outside the 50–150 ft radius range; these values act as hard movement limits.

## Outputs
A warning appears when the suspended load is exactly 90% of the capacity at the current radius. Crossing that threshold is also shown clearly as a caution state.

The game screen must show the complete example load table at all times during play. Display every radius and capacity row:

| Radius (ft) | Capacity (lb) |
|---|---:|
| 50 | 20,000 |
| 75 | 13,000 |
| 100 | 9,000 |
| 125 | 7,000 |
| 150 | 5,500 |

The table must remain visible beside or below the crane scene, not hidden behind a menu. Mark the current radius and its looked-up capacity on or beside the table while play is active.

A dramatic crane tip-over occurs when the load reaches or exceeds 100% of capacity. After the explosion and tip-over animation, the app automatically resets the current level to its starting crane position and starting load layout. Previously delivered loads on that level are also reset.

Each round includes:
- A 3-minute countdown timer that resets for each level
- A current score of 1 point per pound delivered
- The current load weight
- The current radius
- Current chart capacity and safety percentage
- An on-screen load chart with the current radius and load marked
- Delivery progress and the active level
- Per-level wind strength and direction

## Look and feel
The app is a fun, playful construction game with a yellow crane and a building under construction. It uses a clear side view and includes five distinct building levels. Each level has its own visible construction outline and labeled marked delivery positions.

The game has a light mode and a dark mode. It includes a visible theme toggle so the player can switch between bright, high-contrast construction colors and a darker, night-construction palette.

When the crane falls, show a huge, dramatic explosion with expanding fire and smoke effects, debris, and screen shake. When the player passes a level, celebrate with confetti that bursts across the screen.

Four preset load options—4,000, 6,000, 8,000, and 10,000 lb—appear at the staging area each level. The player chooses any two loads to deliver to the two marked unloading positions before advancing. Delivered loads remain at their target positions. Undelivered loads or loads returned after an invalid placement use the staging conveyor.

Wind varies by level and makes a suspended load swing like a pendulum in the horizontal plane.
Loads are picked up by positioning the hook above a staging load and pressing Enter. A load is delivered by precisely positioning it within the matching labeled location on the building outline and pressing Enter.

The player must deliver a load to every marked position to pass a level. Pressing Enter at an incorrect position or dropping a load outside a marked position returns the load to the staging conveyor. The level timer continues until every position is filled or time expires.

A level is passed after every marked position is filled. The app stops play briefly, shows confetti across the screen, and advances to the next level layout.

At the first launch, show an instructions popup explaining the WASD, arrow, and Enter controls, the load-chart warning and tip limits, and the goal of delivering every load. The player must close this popup and press Start Level before the first timer begins.

Before each level begins, show a start screen with the level number and Start Level button. Crane movement and the timer remain paused until Start Level is pressed.

When all two staged loads in a level have been delivered to matching positions, show confetti and a between-level confirmation screen. The player must press Continue / Next Level to advance; the app does not advance automatically.

Each level must provide four staged-load options and exactly two marked unload positions. The player must deliver two loads to complete the level. Retry and reset actions restore the level's staged loads, unload positions, 3-minute timer, and crane position.

## Validation
Use the conservative next-larger-radius rule for all radii:

1. **62 ft:** 62 ft is above 50 ft and at or below 75 ft, so it uses the 75 ft capacity. Allowed load is 13,000 lb. Warning threshold is exactly 11,700 lb (`13,000 x 0.90`). Tip-over begins at 13,000 lb.
2. **125 ft:** 125 ft is exactly in the table, so it uses the 125 ft capacity. Allowed load is 7,000 lb. Warning threshold is exactly 6,300 lb (`7,000 x 0.90`). Tip-over begins at 7,000 lb.
3. **138 ft:** 138 ft is above 125 ft and at or below 150 ft, so it uses the 150 ft capacity. Allowed load is 5,500 lb. Warning threshold is exactly 4,950 lb (`5,500 x 0.90`). Tip-over begins at 5,500 lb.

Implement and test boundary behavior at 89.9%, 90%, 99.9%, and 100% of capacity. Verify the app does not warn below 90%, warns at exactly 90%, does not tip below 100%, and tips at 100% or above.

### Radius and capacity validation results — 2026-11-23

The calculation functions in `crane_calculations.py` passed these checks:

| Radius (ft) | Calculated capacity (lb) | Result |
|---:|---:|---|
| 50 | 20,000 | Pass |
| 50.001, 62, 75 | 13,000 | Pass |
| 75.001, 100 | 9,000 | Pass |
| 100.001, 125 | 7,000 | Pass |
| 125.001, 138, 150 | 5,500 | Pass |

At each of 62, 125, and 138 ft, the 89.9%, 90%, 99.9%, 100%, and 100.1% load cases passed: caution begins at 90%, and overload begins at 100%. The 90% warning loads were 11,700 lb, 6,300 lb, and 4,950 lb respectively; the 100% loads were 13,000 lb, 7,000 lb, and 5,500 lb. Clamping at 50 and 150 ft passed, and capacity lookups outside that range raised `ValueError`.

A Tkinter check with an injected 6,300 lb test load also passed: at 100 ft it was safe against 9,000 lb, just above 100 ft it showed caution against 7,000 lb, and just above 125 ft it triggered the overload warning and level reset against 5,500 lb. The 6,300 lb load was injected for validation and is not a preset. An earlier check incorrectly expected an 8,000 lb load at just above 100 ft to show caution; it exceeds the 7,000 lb capacity and correctly shows the tip limit instead.

**Known discrepancy:** The application passes its trolley-radius value to the load chart, while the specification defines radius as horizontal distance from the tower center to the hook or suspended load. Swing projection and wind can make those values differ. These checks validate the lookup and thresholds for the supplied radius; they do not establish that the displayed load's geometry complies with that definition. Tip-over animation was not validated.

Also test delivery scoring and both pickup/setdown states:
- A delivered load awards 1 point per pound of load weight.
- If a level timer reaches zero, end the level and offer a retry or restart action.
- A load can only be set down in its precisely matching level position.
- An incorrect target or dropped outside a target returns the load to the staging conveyor.
- Resetting after tip-over restores the current level's initial crane and load layout.
- Check that every marked position must be filled before the level is passed and confetti appears.
- Check that the computer-controlled second crane moves predictably and collides are detected.
- Warning and tip calculations update immediately as radius or suspended-load weight changes.

## Build stages

### Stage 1: Desktop UI layout
Build the Tkinter layout for the crane scene, construction building, staging area, status panel, complete load table, timer, score, active level, theme toggle, and persistent keyboard controls. Use Tkinter for the application UI and matplotlib for any charts or plotted visualizations; use numpy where numeric simulation or calculations benefit from it.

**Check:** The full chart and controls remain visible in the desktop window, both themes have readable contrast, and the interface remains usable when the window is resized.

### Stage 2: Crane movement and keyboard controls
Add WASD handlers for trolley and hook movement and arrow-key handlers for jib movement. A/D move screen-left/screen-right, W/S raise/lower the hook, arrow keys swing the jib, and Enter picks up or sets down. Enforce the 50–150 ft hard radius limits and display the live hook position and radius.

**Check:** A/D, W/S, the left/right arrow keys, and Enter work consistently. Continuous keyboard movement works, and movement stops at radius limits.

### Stage 3: Loads, wind, pickup, and delivery
Implement two randomized loads weighing 4,000 and 6,000 lb. Add the staging conveyor, pendulum-style wind, Enter pickup/setdown action, precise target matching, invalid-placement returns, and delivered-load locking.

**Check:** Loads attach and detach correctly; wind visibly affects suspended loads; wrong targets return loads to staging; only exact matching positions accept loads; and delivered loads remain fixed in place.

### Stage 4: Chart safety, scoring, timer, and levels
Implement conservative next-larger-radius capacity lookup, live chart marks, exact 90% warning, 100% tip-over, 1-point-per-pound scoring, reset-per-level 3-minute timers, and five building layouts.

**Check:** 62 ft uses 13,000 lb with warning at 11,700 lb, 125 ft uses 7,000 lb with warning at 6,300 lb, and 138 ft uses 5,500 lb with warning at 4,950 lb. Verify 89.9%, 90%, 99.9%, and 100% boundaries, timer behavior, and level completion.

### Stage 5: Effects, second crane, and final polish
Add the predictable computer-controlled second crane and collision detection, huge tip-over explosion with debris and screen shake, automatic level reset after tipping, confetti after level completion, retry handling, and final desktop-layout and theme polish.

**Check:** The second crane follows a predictable path and collisions are detected. Tip-over triggers at capacity and resets the level with a dramatic effect. Filling every marked position triggers confetti and waits for the player to confirm continuing to the next level. Both themes and all five layouts are playable in the desktop application.

## Out of scope
This is a fictional game example, not a source of legitimate crane specifications or lifting instructions.
## Platform

This is a Python desktop application built with Tkinter, numpy, and matplotlib. Start it with `python app.py`.
- Python desktop app using Tkinter, started with `python app.py`
- Calculations with numpy, kept in their own module, separate from
  the window code
- Diagrams drawn with matplotlib, embedded in the window
