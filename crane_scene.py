"""Matplotlib crane scene and load-chart view embedded in Tkinter."""

import math
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from crane_calculations import LOAD_CHART


class CraneScene:
    def __init__(self, parent):
        self.figure = Figure(figsize=(9.2, 5.2), dpi=90, constrained_layout=True)
        self.scene = self.figure.add_subplot(121)
        self.chart = self.figure.add_subplot(122)
        self.widget = FigureCanvasTkAgg(self.figure, master=parent)
        self.widget.get_tk_widget().pack(fill="both", expand=True)
        self.theme = "light"
        self.phase = 0.0

    def draw(self, state, radius, height, angle, load_weight, capacity):
        dark = self.theme == "dark"
        bg, fg = ("#111827", "#f4f7fb") if dark else ("#eef2f6", "#172033")
        panel, sky = ("#1c2535", "#1b3550") if dark else ("#ffffff", "#dff3fb")
        for ax in (self.scene, self.chart):
            ax.clear()
            ax.set_facecolor(panel)
            ax.tick_params(colors=fg, labelsize=8)
            for spine in ax.spines.values():
                spine.set_color(fg)
        self.figure.set_facecolor(bg)
        ax = self.scene
        ax.set_xlim(35, 165)
        ax.set_ylim(0, 120)
        ax.set_facecolor(sky)
        ax.set_title(f"Tower Crane · Level {state.level}", color=fg)
        ax.axhspan(0, 8, color="#b49565")
        # Construction outline changes by level.
        floors = 2 + (state.level - 1) % 4
        for floor in range(floors):
            y = 18 + floor * 16
            ax.add_patch(Rectangle((105, y), 24, 13,
                facecolor="#8996a5", edgecolor=fg, alpha=.8))
            ax.text(117, y + 6, "A" if floor % 2 == 0 else "B", ha="center", color=fg, fontsize=9)
        ax.plot([50, 50], [8, 108], color="#ffd21f", linewidth=7, solid_capstyle="round")
        ax.plot([50, 145], [108, 108], color="#ffd21f", linewidth=6)
        ax.add_patch(Rectangle((48, 8), 5, 100,
            facecolor="#ffd21f", edgecolor="#d69c00"))
        trolley = 50 + (radius - 50) * math.cos(angle)
        ax.plot([trolley, trolley], [108, height], color=fg, linewidth=1.5)
        ax.scatter([trolley], [108], marker="s", s=70, color="#dc4c5a", zorder=5)
        sway = 0
        if state.carried is not None:
            sway = math.sin(self.phase) * state.wind * state.wind_direction * 1.5
        hx = trolley + sway
        ax.plot([hx], [height], marker="v", markersize=9, color="#dc4c5a")
        if state.carried is not None:
            weight = state.loads[state.carried].weight_lb
            ax.add_patch(Rectangle((hx - 4, height - 8), 8, 7,
                facecolor="#be8b19", edgecolor=fg))
            ax.text(hx, height - 5, f"{weight//1000}k", ha="center", va="center", fontsize=7)
        # Staging conveyor and four choices.
        ax.plot([54, 72], [14, 14], color="#596579", linewidth=5)
        for i, item in enumerate(state.loads):
            if item.delivered_to is not None or (state.carried == i):
                continue
            x = 56 + i * 4.5
            ax.scatter([x], [18], s=95, marker="s", color="#be8b19" if item.selected else "#d69c00")
            ax.text(x, 23, f"{item.weight_lb//1000}k", ha="center", fontsize=7, color=fg)
        for i, target in enumerate(state.targets):
            filled = any(item.delivered_to == i for item in state.loads)
            ax.scatter([target.radius_ft], [target.height_ft], s=160, marker="s",
                       facecolors="#2aa876" if filled else "none", edgecolors="#2aa876", linewidths=2)
            ax.text(target.radius_ft, target.height_ft + 8, target.label, ha="center", color=fg)
        # Predictable, independent second crane cycle.
        self.phase += .06
        other_x = 82 + 20 * math.sin(self.phase / 2)
        ax.plot([other_x, other_x], [70, 100], color="#4a70b5", linewidth=4)
        ax.plot([other_x, other_x + 22], [100, 100], color="#4a70b5", linewidth=4)
        ax.set_xlabel("Crane radius (ft)", color=fg)
        ax.grid(alpha=.18)
        ax.text(0.02, .97, f"Wind: {state.wind} · {'→' if state.wind_direction > 0 else '←'}",
                transform=ax.transAxes, va="top", color=fg)

        ca = self.chart
        radii = [row[0] for row in LOAD_CHART]
        capacities = [row[1] for row in LOAD_CHART]
        ca.plot(capacities, radii, marker="o", color="#4a70b5")
        ca.set_title("Load chart", color=fg)
        ca.set_xlabel("Capacity (lb)", color=fg)
        ca.set_ylabel("Radius (ft)", color=fg)
        ca.set_yticks(radii)
        ca.grid(alpha=.25)
        ca.invert_xaxis()
        ca.axhline(radius, color="#dc4c5a", linestyle="--", linewidth=1)
        ca.scatter([capacity], [radius], color="#dc4c5a", s=55, zorder=5)
        ca.text(.05, .05, "Radius  Capacity (lb)\n" + "\n".join(f"{r:>3.0f} ft      {c:,}" for r, c in LOAD_CHART),
                transform=ca.transAxes, fontsize=8, color=fg, va="bottom",
                bbox={"facecolor": panel, "alpha": .85, "edgecolor": fg})
        if load_weight and capacity:
            fraction = load_weight / capacity
            ca.text(.04, .96, f"Load: {load_weight:,} lb · {fraction:.1%}", transform=ca.transAxes,
                    va="top", color="#dc4c5a" if fraction >= .9 else fg)
        self.widget.draw_idle()

