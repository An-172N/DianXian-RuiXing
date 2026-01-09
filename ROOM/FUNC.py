from typing import Callable, Any


def preload(stack: list, func: Callable[[str], Any], *args: Any) -> dict:
    """
    预加载多个文件，func为加载函数
    stack列表存有若干个由项名和文件名组成一对的集合
    """

    return {key: func(file, *args) for key, file in stack}


def delta(minuend: tuple, subtrahend: tuple) -> tuple:
    """
    计算minuend元组和subtrahend元组对应元素的值差
    要确保两个元组的项数都一致
    """

    return tuple(i - j for i, j in zip(minuend, subtrahend))


def fibonacci(former: float, latter: float, frequency: int) -> tuple:
    """
    计算广义斐波那契数列的第frequency和第frequency + 1项
    former和latter可以是浮点数
    """

    for _ in range(frequency):
        former, latter = latter, former + latter

    return former, latter


def divide(dividend: float, divisor: float, default: float) -> float:
    """
    除法计算，但可以安全地除
    推荐default参数为浮点类型
    """

    return dividend / divisor if divisor != 0 else default


def digital(count: int, cycle: int, duty: float) -> bool:
    """
    根据cycle对count计算为对应的数字信号值
    duty的范围指定为0到1区间时使用最佳
    """

    return count % cycle < cycle * duty


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    限制value在maximum和minimum之间
    如果minimum大于maximum会把这两个参数反转
    """

    minimum, maximum = min(minimum, maximum), max(minimum, maximum)

    return max(min(value, maximum), minimum)