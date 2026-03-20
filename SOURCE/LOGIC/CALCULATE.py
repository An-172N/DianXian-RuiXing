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

    if (distance := math.hypot(dx, dy)) < step:
        return (tx, ty), (dx, dy)
    else:
        if distance > 0:
            dx, dy = dx / distance, dy / distance

        return (cx + dx * step, cy + dy * step), (dx, dy)


def translate(
    points: list[tuple[float, float]],
    target: tuple[float, float]
) -> list[tuple[float, float]]:
    x1, y1 = points[0]
    x2, y2 = points[-1]
    tx, ty = target
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    return [(x + (tx - cx), y + (ty - cy)) for (x, y) in points]


def rotate(
    points: list[tuple[float, float]],
    degree: float,
    center: tuple[float, float] = None
) -> list[tuple[float, float]]:
    radians = math.radians(degree)
    cos = math.cos(radians)
    sin = math.sin(radians)

    if center is None:
        number = len(points)
        cx, cy = sum(point[0] for point in points) / number, sum(point[1] for point in points) / number
    else:
        cx, cy = center

    return [(cx + (x - cx) * cos - (y - cy) * sin, cy + (x - cx) * sin + (y - cy) * cos) for x, y in points]


def approximate(
    value: float,
    limit: int = 180,
    step: int = 10
) -> int:
    return 0 if (rounded := round((value % limit) / step) * step) == limit else rounded


def bearing(
    x: float,
    y: float
) -> float:
    return math.degrees(math.atan2(x, y)) % 360


def add(
    *packs: tuple[float, ...] | list[float] | set[float]
) -> tuple[float, ...]:
    return tuple(map(sum, zip(*packs)))


def clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    return max(min(value, max(minimum, maximum)), min(minimum, maximum))


def fibonacci(
    former: float,
    latter: float,
    frequency: int
) -> float:
    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)