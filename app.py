"""Tkinter entry point for the Tower Crane Challenge."""

import time
import tkinter as tk
from tkinter import messagebox
import math

from crane_calculations import clamp_radius, capacity_at_radius, is_caution, is_overloaded
from crane_scene import CraneScene
from game_state import GameState


class CraneApp:
    def __init__(self, root):
        self.root = root
        root.title("Tower Crane Challenge")
        root.geometry("1120x760")
        root.minsize(820, 620)
        self.state = GameState()
        self.radius = 75.0
        self.height = 30.0
        self.angle = 0.0
        self.held = set()
        self.last = time.monotonic()
        self.dark = False

        self.main = tk.Frame(root, padx=8, pady=8)
        self.main.pack(fill="both", expand=True)
        self.toolbar = tk.Frame(self.main)
        self.toolbar.pack(fill="x")
        self.title_label = tk.Label(self.toolbar, text="Tower Crane Challenge", font=("TkDefaultFont", 16, "bold"))
        self.title_label.pack(side="left")
        self.theme_button = tk.Button(self.toolbar, text="Dark mode", command=self.toggle_theme)
        self.theme_button.pack(side="right", padx=4)
        self.retry_button = tk.Button(self.toolbar, text="Retry Level", command=self.retry)
        self.retry_button.pack(side="right", padx=4)
        self.start_button = tk.Button(self.toolbar, text="Start Level", command=self.start)
        self.start_button.pack(side="right", padx=4)
        self.next_button = tk.Button(self.toolbar, text="Continue / Next Level", command=self.next_level)
        self.next_button.pack(side="right", padx=4)

        self.body = tk.Frame(self.main)
        self.body.pack(fill="both", expand=True)
        self.scene = CraneScene(self.body)
        self.status = tk.StringVar()
        tk.Label(self.main, textvariable=self.status, anchor="w", font=("TkDefaultFont", 10, "bold")).pack(fill="x")
        self.load_bar = tk.Frame(self.main)
        self.load_bar.pack(fill="x", pady=4)
        self.load_buttons = []
        self.refresh_load_buttons()
        self.controls = tk.Label(self.main,
            text="Controls: A/D trolley · W/S hook · ←/→ swing jib · Enter pick up / set down · choose two staged loads",
            anchor="w", justify="left", wraplength=1000)
        self.controls.pack(fill="x", pady=(4, 0))

        root.bind_all("<KeyPress>", self.key_down)
        root.bind_all("<KeyRelease>", self.key_up)
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        self.refresh()
        messagebox.showinfo("How to play", "Choose two of the four staged loads. Use A/D to move, W/S to raise or lower the hook, and the arrow keys to swing. Press Enter to pick up or deliver. Capacity caution starts at 90%; the crane tips at 100%. Deliver both loads to pass the level.", parent=root)
        self.root.after(30, self.loop)

    def refresh_load_buttons(self):
        for widget in self.load_bar.winfo_children():
            widget.destroy()
        self.load_buttons = []
        for i, load in enumerate(self.state.loads):
            text = f"{'✓ ' if load.selected else ''}{load.weight_lb:,} lb"
            button = tk.Button(self.load_bar, text=text, command=lambda j=i: self.toggle_load(j))
            button.pack(side="left", padx=3)
            self.load_buttons.append(button)

    def toggle_load(self, index):
        self.state.toggle_load(index)
        self.refresh_load_buttons()
        self.refresh()

    def start(self):
        if self.state.start():
            self.start_button.config(state="disabled")
        else:
            messagebox.showinfo("Select loads", self.state.message, parent=self.root)
        self.refresh()

    def retry(self):
        self.state.retry()
        self.radius, self.height, self.angle = 75.0, 30.0, 0.0
        self.start_button.config(state="normal")
        self.refresh_load_buttons()
        self.refresh()

    def next_level(self):
        self.state.advance()
        self.radius, self.height, self.angle = 75.0, 30.0, 0.0
        self.start_button.config(state="normal")
        self.refresh_load_buttons()
        self.refresh()

    def key_down(self, event):
        key = event.keysym.lower()
        if key in ("a", "d", "w", "s", "left", "right"):
            self.held.add(key)
        elif key == "return" and self.state.running:
            self.enter_action()

    def key_up(self, event):
        self.held.discard(event.keysym.lower())

    def nearest_target(self):
        hook_x = self.horizontal_position()
        for i, target in enumerate(self.state.targets):
            if any(load.delivered_to == i for load in self.state.loads):
                continue
            if abs(hook_x - target.radius_ft) <= 4 and abs(self.height - target.height_ft) <= 6:
                return i
        return None

    def horizontal_position(self):
        """Side-view projection of the jib trolley position."""
        return 50 + (self.radius - 50) * math.cos(self.angle)

    def enter_action(self):
        if self.state.carried is None:
            if abs(self.radius - 60) > 12 or self.height > 32:
                self.state.message = "Move over the staging conveyor and lower the hook to pick up a load."
            elif self.state.pickup() is not None:
                self.state.message = "Load picked up. Move it to a matching target."
        else:
            outcome, _ = self.state.set_down(self.nearest_target())
            if outcome == "delivered" and self.state.finished:
                self.next_button.config(state="normal")
        self.refresh_load_buttons()
        self.refresh()

    def toggle_theme(self):
        self.dark = not self.dark
        self.scene.theme = "dark" if self.dark else "light"
        self.theme_button.config(text="Light mode" if self.dark else "Dark mode")
        self.refresh()

    def loop(self):
        now = time.monotonic()
        dt = min(.1, now - self.last)
        self.last = now
        if self.state.running:
            speed = 35 * dt
            self.radius = clamp_radius(self.radius + speed * (int("d" in self.held) - int("a" in self.held)))
            self.height = max(12, min(100, self.height + speed * 1.3 * (int("w" in self.held) - int("s" in self.held))))
            self.angle = max(-1.1, min(1.1, self.angle +
                (int("right" in self.held) - int("left" in self.held)) * dt * .8))
            self.state.tick(dt)
            weight = self.state.loads[self.state.carried].weight_lb if self.state.carried is not None else 0
            cap = capacity_at_radius(self.radius)
            if weight and is_overloaded(weight, cap):
                messagebox.showwarning("Crane overload", "The load reached the crane capacity. The level has reset.", parent=self.root)
                self.state.retry()
                self.radius, self.height = 75.0, 30.0
                self.refresh_load_buttons()
            elif self.collision_detected():
                self.state.running = False
                self.state.finished = True
                self.state.won = False
                self.state.message = "Collision with the second crane. Retry the level."
            if self.state.finished:
                self.start_button.config(state="normal")
        self.refresh()
        self.root.after(30, self.loop)

    def collision_detected(self):
        """Conservative hook/boom clearance check against the visible crane path."""
        other_x = 82 + 20 * math.sin(self.scene.phase / 2)
        hook_x = self.horizontal_position()
        if 70 <= self.height <= 106 and abs(hook_x - other_x) < 4:
            return True
        if self.state.carried is not None and 96 <= self.height <= 104:
            return abs(hook_x - other_x) < 24 and hook_x >= other_x
        return False

    def refresh(self):
        capacity = capacity_at_radius(self.radius)
        weight = self.state.loads[self.state.carried].weight_lb if self.state.carried is not None else 0
        caution = is_caution(weight, capacity) if weight else False
        minutes, seconds = divmod(int(self.state.remaining), 60)
        condition = "TIP LIMIT" if weight and is_overloaded(weight, capacity) else ("CAUTION ≥90%" if caution else "Safe")
        carried_text = f"{weight:,} lb" if weight else "None"
        safety = f"    Safety {weight/capacity:.1%}" if weight else ""
        self.status.set(
            f"Level {self.state.level}/5    Time {minutes:02d}:{seconds:02d}    Score {self.state.score:,}    "
            f"Carried {carried_text}    Radius {self.radius:.1f} ft    Capacity {capacity:,} lb{safety}    "
            f"{condition}    Delivered {self.state.delivered_count}/2    Wind {self.state.wind} · "
            f"{'→' if self.state.wind_direction > 0 else '←'}    {self.state.message}"
        )
        self.scene.draw(self.state, self.radius, self.height, self.angle, weight, capacity)
        self.start_button.config(state="normal" if not self.state.running and not self.state.finished else "disabled")
        self.retry_button.config(state="normal")
        self.next_button.config(state="normal" if self.state.won else "disabled")
        self.root.configure(bg="#111827" if self.dark else "#eef2f6")


def main():
    root = tk.Tk()
    CraneApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
