def delta_tuple(tuple1: tuple, tuple2: tuple) -> tuple:
    return tuple(
        i - j
        for i, j in zip(tuple1, tuple2)
    )


def fibonacci(a: float, b: float, n: int) -> float:
    for _ in range(2, n):
        a, b = b, a + b

    return a, b


def divide(dividend: float, divisor: float, default: float) -> float:
    return (
        dividend / divisor
        if divisor != 0 
        else 
        default
    )