"""Pure crane radius and load-chart calculations."""

from bisect import bisect_left

LOAD_CHART = ((50.0, 20_000), (75.0, 13_000), (100.0, 9_000), (125.0, 7_000), (150.0, 5_500))
MIN_RADIUS_FT = LOAD_CHART[0][0]
MAX_RADIUS_FT = LOAD_CHART[-1][0]
WARNING_FRACTION = 0.90


def clamp_radius(radius_ft: float) -> float:
    return max(MIN_RADIUS_FT, min(MAX_RADIUS_FT, float(radius_ft)))


def capacity_at_radius(radius_ft: float) -> int:
    """Return capacity at the next chart radius, rounding up conservatively."""
    radius = float(radius_ft)
    if not MIN_RADIUS_FT <= radius <= MAX_RADIUS_FT:
        raise ValueError("radius must be between 50 and 150 ft")
    index = bisect_left([row[0] for row in LOAD_CHART], radius)
    return LOAD_CHART[index][1]


def load_fraction(load_lb: float, capacity_lb: float) -> float:
    if capacity_lb <= 0:
        raise ValueError("capacity must be positive")
    return max(0.0, float(load_lb)) / capacity_lb


def is_caution(load_lb: float, capacity_lb: float) -> bool:
    return load_fraction(load_lb, capacity_lb) >= WARNING_FRACTION


def is_overloaded(load_lb: float, capacity_lb: float) -> bool:
    return load_lb >= capacity_lb

