def delta_position(target_position, source_position):
    """
    计算二维坐标差
    
    Args:
        target_position: 目标对象的二维坐标元组
        source_position: 源头对象的二维坐标元组

    Returns:
        两点 x 和 y 的差值
    """

    dx = target_position[0] - source_position[0]
    dy = target_position[1] - source_position[1]

    return dx, dy


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