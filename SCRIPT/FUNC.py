# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


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