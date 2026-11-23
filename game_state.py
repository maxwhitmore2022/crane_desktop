"""State and rules for the crane delivery game."""

from dataclasses import dataclass
import random

LOAD_CHOICES = (4_000, 6_000, 8_000, 10_000)
LEVEL_SECONDS = 180
TARGET_X_TOLERANCE = 5.0
TARGET_HEIGHT_TOLERANCE = 8.0
TARGET_SWING_TOLERANCE = 0.20


@dataclass
class Load:
    weight_lb: int
    selected: bool = False
    delivered_to: int | None = None


@dataclass(frozen=True)
class Target:
    label: str
    radius_ft: float
    height_ft: float
    swing: float


class GameState:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.wind = 1.0
        self.wind_direction = 1
        self.targets: list[Target] = []
        self.loads: list[Load] = []
        self.carried: int | None = None
        self.remaining = LEVEL_SECONDS
        self.running = False
        self.finished = False
        self.won = False
        self.message = ""
        self.setup_level(1)

    def setup_level(self, level: int, selected_weights=None) -> None:
        self.level = level
        rng = random.Random(4100 + level)
        selected_weights = selected_weights if selected_weights is not None else random.sample(LOAD_CHOICES, 2)
        self.loads = [Load(weight, selected=weight in selected_weights) for weight in LOAD_CHOICES]
        self.targets = [
            Target("A", 60 + (level - 1), 25 + (level % 3) * 8, -0.6),
            Target("B", 70 + (level - 1), 55 + ((level + 1) % 3) * 7, 0.6),
        ]
        self.wind = round(rng.uniform(0.5, 2.2), 1)
        self.wind_direction = rng.choice((-1, 1))
        self.carried = None
        self.remaining = LEVEL_SECONDS
        self.running = False
        self.finished = False
        self.won = False
        self.message = "Two loads selected. Press Start Level."

    @property
    def selected_count(self) -> int:
        return sum(load.selected for load in self.loads)

    @property
    def delivered_count(self) -> int:
        return sum(load.delivered_to is not None for load in self.loads)

    def toggle_load(self, index: int) -> bool:
        load = self.loads[index]
        if self.running or self.finished or self.carried is not None or load.delivered_to is not None:
            return False
        if load.selected:
            load.selected = False
            return True
        if self.selected_count >= 2:
            self.message = "Choose only two loads per level."
            return False
        load.selected = True
        return True

    def start(self) -> bool:
        if self.selected_count != 2:
            self.message = "Select exactly two loads before starting."
            return False
        if self.finished:
            return False
        self.running = True
        self.message = ""
        return True

    def pickup(self) -> int | None:
        if not self.running or self.carried is not None:
            return None
        for i, load in enumerate(self.loads):
            if load.selected and load.delivered_to is None:
                self.carried = i
                return i
        return None

    def set_down(self, target_index: int | None) -> tuple[str, int | None]:
        if not self.running or self.carried is None:
            return ("none", None)
        index = self.carried
        self.carried = None
        load = self.loads[index]
        if target_index is not None and 0 <= target_index < len(self.targets) and not any(
            item.delivered_to == target_index for item in self.loads
        ):
            load.delivered_to = target_index
            self.score += load.weight_lb
            if self.delivered_count == 2:
                self.running = False
                self.finished = True
                self.won = True
                self.message = "All levels complete!" if self.level == 5 else "Level complete! Continue when ready."
            return ("delivered", index)
        self.message = "Invalid placement. Load returned to staging."
        return ("returned", index)

    def tick(self, seconds: float = 1.0) -> bool:
        if not self.running:
            return False
        self.remaining = max(0, self.remaining - seconds)
        if self.remaining == 0:
            self.running = False
            self.finished = True
            self.won = False
            self.message = "Time expired. Retry the level."
            return True
        return False

    def retry(self) -> None:
        self.score -= sum(load.weight_lb for load in self.loads if load.delivered_to is not None)
        self.setup_level(self.level, [load.weight_lb for load in self.loads if load.selected])

    def advance(self) -> None:
        if self.won and self.level < 5:
            self.setup_level(self.level + 1)

