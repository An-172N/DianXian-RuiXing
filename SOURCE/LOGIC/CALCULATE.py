# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import math


def vector(
    current: tuple[float, float],
    target: tuple[float, float],
    step: int,
) -> tuple[tuple[float, float], tuple[float, float]]:
    cx, cy = current
    tx, ty = target
    dx, dy = tx - cx, ty - cy
    dist_sq = dx * dx + dy * dy

    if dist_sq < step * step:
        return (tx, ty), (dx, dy)

    distance = math.sqrt(dist_sq)
    if distance > 0:
        dx, dy = dx / distance, dy / distance

    return (cx + dx * step, cy + dy * step), (dx, dy)


def approximate(
    value: float,
    limit: int = 180,
    step: int = 15
) -> int:
    return 0 if (rounded := round((value % limit) / step) * step) == limit else int(rounded)


def clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    if maximum < minimum:
        maximum, minimum = minimum, maximum
    if value > maximum:
        return maximum
    elif value < minimum:
        return minimum
    else:
        return value


def fibonacci(
    former: float,
    latter: float,
    frequency: int
) -> float:
    for _ in range(0, frequency + 1):
        former, latter = latter, former + latter

    return former


def direct(
    x: float,
    y: float
) -> float:
    return math.degrees(math.atan2(x, y)) % 360