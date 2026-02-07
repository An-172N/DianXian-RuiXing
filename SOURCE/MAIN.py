# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import sys


sys.dont_write_bytecode = True
for module in ['numpy', 'timidity', 'pygame.examples']:
    sys.modules[module] = None


def main() -> int:
    import pygame

    clock = pygame.time.Clock()

    pygame.display.init()
    pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')
    pygame.font.init()

    screen = pygame.display.set_mode((480, 360), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED, vsync=1)

    import KERNEL

    KERNEL.update(clock, screen)

    return 0


if __name__ == "__main__":
    main()