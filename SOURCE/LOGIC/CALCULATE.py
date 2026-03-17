# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import math


def vector(
    current: tuple[int | float, int | float],
    target: tuple[int | float, int | float],
    delay: int | float,
) -> tuple[tuple[int | float, int | float], tuple[int | float, int | float]]:
    cx, cy = current
    tx, ty = target
    dx, dy = tx - cx, ty - cy

    if (distance := math.hypot(dx, dy)) < delay:
        return (tx, ty), (dx, dy)
    else:
        if distance > 0:
            dx, dy = dx / distance, dy / distance

        return (cx + dx * delay, cy + dy * delay), (dx, dy)
    

def center(
    points: list[tuple[int | float, int | float]],
    target: tuple[int | float, int | float]
) -> list[tuple[int | float, int | float]]:
    x1, y1 = points[0]
    x2, y2 = points[-1]
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    return [(x + (target[0] - cx), y + (target[1] - cy)) for (x, y) in points]


def rotate(
    points: list[tuple[int | float, int | float]],
    degree: int | float,
    center: tuple[int | float, int | float] = None
) -> list[tuple[int | float, int | float]]:
    radians = math.radians(degree)
    cos = math.cos(radians)
    sin = math.sin(radians)

    if center is None:
        number = len(points)
        cx, cy = sum(p[0] for p in points) / number, sum(p[1] for p in points) / number
    else:
        cx, cy = center

    return [(cx + (x - cx) * cos - (y - cy) * sin, cy + (x - cx) * sin + (y - cy) * cos) for x, y in points]


def approximate(
    value: int | float,
    limit: int = 180,
    step: int = 6
) -> int:
    return 0 if (rounded := round((value % limit) / step) * step) == limit else rounded


def bearing(
    x: float,
    y: float
) -> float:
    return math.degrees(math.atan2(x, y)) % 360


def add(
    *packs: tuple[int | float, ...] | list[int | float] | set[int | float]
) -> tuple[int | float, ...]:
    return tuple(map(sum, zip(*packs)))


def clamp(
    value: int | float,
    minimum: int | float,
    maximum: int | float
) -> int | float:
    return max(min(value, max(minimum, maximum)), min(minimum, maximum))


def fibonacci(
    former: int | float,
    latter: int | float,
    frequency: int
) -> int | float:
    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)