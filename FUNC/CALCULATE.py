def delta_tuple(first_tuple, second_tuple):
    dx = first_tuple[0] - second_tuple[0]
    dy = first_tuple[1] - second_tuple[1]
    dz = first_tuple[2] - second_tuple[2]

    return dx, dy, dz


def fibonacci(first_number, second_number, frequency):
    previous_number = first_number
    current_number = second_number

    for _ in range(2, frequency):
        next_number = previous_number + current_number
        previous_number = current_number
        current_number = next_number

    return current_number


def divide(dividend, divisor, default):
    if divisor != 0:
        result = dividend / divisor

        return result
    else:
        return default