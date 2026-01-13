# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


def wise(calculate: object, *tuples: tuple) -> tuple:
    """
    对*tuples元组的对应元素用calculate函数进行计算操作 \n
    calculate函数会接收由对应项组成的元组
    """

    return tuple(calculate(i) for i in zip(*tuples))


def fibonacci(former: int, latter: int, frequency: int) -> int:
    """
    计算广义斐波那契数列的第frequency项 \n
    former和latter可以是浮点数
    """

    return former if frequency <= 0 else fibonacci(latter, former + latter, frequency - 1)


def clamp(value: float, minimum: float, maximum: float) -> float:
    """
    限制value在minimum和maximum之间 \n
    如果minimum大于maximum会把这两个参数反转
    """

    return max(min(value, max(minimum, maximum)), min(minimum, maximum))