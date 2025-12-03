def delta_tuple(first_tuple: tuple, second_tuple: tuple) -> tuple:
    dx = first_tuple[0] - second_tuple[0]
    dy = first_tuple[1] - second_tuple[1]
    dz = first_tuple[2] - second_tuple[2]

    return dx, dy, dz


def fibonacci(number_a: int, number_b: int, frequency: int) -> int:
    for _ in range(2, frequency):
        next_number = number_a + number_b
        number_a = number_b
        number_b = next_number

    return number_b


def divide(dividend: int|float, divisor: int|float, default: int|float) -> int|float:
    if divisor != 0:
        result = dividend / divisor

        return result
    else:
        return default