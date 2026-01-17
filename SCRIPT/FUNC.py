# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


def add(*tuples: tuple) -> tuple:
    """
    对*tuples元组进行加法运算 \n
    推荐每个元组的长度都一样
    """

    return tuple(map(sum, zip(*tuples)))


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