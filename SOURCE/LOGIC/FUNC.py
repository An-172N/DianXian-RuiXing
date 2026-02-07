# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


def add(*tuples: tuple) -> tuple:
    return tuple(map(sum, zip(*tuples)))


def fibonacci(former: int, latter: int, frequency: int) -> int:
    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(min(value, max(minimum, maximum)), min(minimum, maximum))