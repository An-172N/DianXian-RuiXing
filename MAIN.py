# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import sys


def main() -> int:
    import pygame

    pygame.display.init()
    pygame.font.init()

    pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')

    import SCRIPT.KERNEL

    SCRIPT.KERNEL.update()

    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    for module in ['numpy', 'timidity']:
        sys.modules[module] = None

    main()