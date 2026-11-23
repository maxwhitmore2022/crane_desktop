# Prompt Log

## 2026-11-23

- **Asked:** “test prompts.md”
- **Changed:** Created this prompt-log entry.
- **Worked:** Yes.

- **Asked:** Commit current changes.
- **Changed:** Recorded this request; no commit was created.
- **Worked:** No — Git cannot run because Xcode Command Line Tools are not installed or configured in this environment.

- **Asked:** Commit changes.
- **Changed:** Recorded this retry; no commit was created.
- **Worked:** No — Git still cannot run because Xcode Command Line Tools are not installed or configured in this environment.

- **Asked:** Update `AGENTS.md` for a Tkinter, numpy, and matplotlib Python desktop app started with `python app.py`, remove web-only rules, and retain the prompt-log rule.
- **Changed:** Added the desktop stack and launch command to `AGENTS.md`; retained its prompt-log rule. There were no web-only rules in that file to remove.
- **Worked:** Yes.

- **Asked:** Update `spec.md` for a Tkinter, numpy, and matplotlib Python desktop app started with `python app.py`, remove web-only rules, and retain the prompt-log rule.
- **Changed:** Updated the specification's platform and build-stage requirements for the desktop stack; removed web, mobile, touch, HTML/SVG, and single-file-app requirements. The prompt-log rule remains in `AGENTS.md`.
- **Worked:** Yes.

- **Asked:** Read `spec.md`, list its rules, and distinguish rules for a Python desktop app from web-app-only rules.
- **Changed:** Reviewed the specification and provided the requested applicability analysis; no app code was changed.
- **Worked:** Yes.

- **Asked:** Commit the changes and clear the working tree.
- **Changed:** Added the initial project files (`AGENTS.md`, `index.html`, `prompts.md`, and `spec.md`) to Git and recorded this request.
- **Worked:** Yes — committed as `8284add`; the working tree is clean.

- **Asked:** Implement the plan to build the crane game as a Python Tkinter desktop app.
- **Changed:** Added `app.py`, `game_state.py`, `crane_calculations.py`, and `crane_scene.py` for the desktop UI, game rules, load-chart calculations, and Matplotlib scene/chart. Added load selection, movement, pickup and setdown, scoring, timer, retries and level transitions, theme toggle, wind, second-crane collision checks, and capacity warning/tip handling.
- **Worked:** Python syntax check passed. The app was not launched in this environment, so interactive behavior remains unverified.

- **Asked:** Commit the changes and clear the working tree.
- **Changed:** Recorded this request; staging and commit are pending.
- **Worked:** Yes — committed as `c4d11e0`; the working tree is clean.

- **Asked:** Reported that the app did not work and clarified that controls/gameplay failed broadly.
- **Changed:** Fixed the left/right jib swing so it changes the visible trolley projection and target matching. Reproduced module imports and ran a basic game-state flow through load selection, pickup, two deliveries, and scoring.
- **Worked:** Syntax and basic game-state flow passed; full interactive behavior still needs validation in the user's GUI environment.

- **Asked:** Commit the jib swing fix and related changes.
- **Changed:** Recorded this commit request; staging is pending.
- **Worked:** Pending commit verification.
