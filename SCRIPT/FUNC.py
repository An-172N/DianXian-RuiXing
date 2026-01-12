# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


def delta(minuend: tuple, subtrahend: tuple) -> tuple:
    """
    计算minuend元组和subtrahend元组对应元素的值差 \n
    要确保两个元组的项数都一致
    """

    return tuple(i - j for i, j in zip(minuend, subtrahend))


def fibonacci(former: int, latter: int, frequency: int) -> int:
    """
    计算广义斐波那契数列的第frequency项 \n
    former和latter可以是浮点数
    """

    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)


def divide(dividend: float, divisor: float, default: float) -> float:
    """
    除法计算，但可以安全地除 \n
    推荐default参数为浮点类型
    """

    return dividend / divisor if divisor != 0 else default


def digital(count: int, cycle: int, duty: float) -> bool:
    """
    根据cycle对count计算为对应的数字信号值 \n
    duty的范围指定为0到1区间时使用最佳
    """

    return count % cycle < cycle * duty


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    限制value在minimum和maximum之间 \n
    如果minimum大于maximum会把这两个参数反转
    """

    return max(min(value, max(minimum, maximum)), min(minimum, maximum))