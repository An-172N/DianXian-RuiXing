def delta_tuple(first_tuple, second_tuple):
    """
    计算两个元组内的三个值的值差
    计算方式是 first_tuple 减去 second_tuple
    
    Args:
        first_tuple: 第一个元组
        second_tuple: 第二个元组

    Returns:
        两个元组内的三个值的值差元组
    """

    dx = first_tuple[0] - second_tuple[0]
    dy = first_tuple[1] - second_tuple[1]
    dz = first_tuple[2] - second_tuple[2]

    return (dx, dy, dz)


def fibonacci(first_number, second_number, frequency):
    """
    计算广义斐波那契数列的第 frequency 项

    Args:
        first_number: 数列第一项
        second_number: 数列第二项
        frequency: 要计算的项对值（frequency >= 2

    Returns:
        广义斐波那契数列的第 frequency 项
    """

    previous_number = first_number
    current_number = second_number

    for _ in range(2, frequency):
        next_number = previous_number + current_number
        previous_number = current_number
        current_number = next_number

    return current_number