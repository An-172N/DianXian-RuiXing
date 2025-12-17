def delta_tuple(tuple1: tuple, tuple2: tuple) -> tuple:
    return tuple(
        i - j
        for i, j in zip(tuple1, tuple2)
    )


def fibonacci(a: int, b: int, frequency: int) -> int:
    for _ in range(2, frequency):
        a, b = b, a + b

    return b


def divide(dividend: float, divisor: float, default: float) -> float:
    return (
        dividend / divisor
        if divisor != 0 
        else 
        default
    )