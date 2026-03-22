# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


def main():
    import sys

    sys.dont_write_bytecode = True
    for module in ('numpy', 'timidity', 'pygame.examples'):
        sys.modules[module] = None

    import argparse

    parser = argparse.ArgumentParser()
    for i, j in (('-stage', 1), ('-level', 1), ('-flash', 3), ('-power', 0), ('-seed', None)):
        parser.add_argument(i, type=int, default=j)
    args = parser.parse_args()

    import random

    random.seed(args.seed)

    import pygame

    clock = pygame.time.Clock()

    pygame.display.init()
    pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN|pygame.SCALED, vsync=1)

    import SCRIPT

    SCRIPT.KERNEL.update(clock, screen, (int(args.stage), int(args.level), int(args.flash), int(args.power)))


if __name__ == "__main__":
    main()