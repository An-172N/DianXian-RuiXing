# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


def main() -> int:
    import sys

    sys.dont_write_bytecode = True
    for module in ['numpy', 'timidity', 'pygame.examples']:
        sys.modules[module] = None

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-stage', type=int, default=1)
    parser.add_argument('-level', type=int, default=0)
    parser.add_argument('-flash', type=int, default=3)
    parser.add_argument('-power', type=int, default=0)
    parser.add_argument('-seed', type=int, default=None)

    args = parser.parse_args()

    import random

    random.seed(args.seed)

    import pygame

    clock = pygame.time.Clock()

    pygame.display.init()
    pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')
    pygame.font.init()

    screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN|pygame.SCALED, vsync=1)

    import SCRIPT

    SCRIPT.KERNEL.update(clock, screen, (int(args.stage), int(args.level), int(args.flash), int(args.power)))

    return 0


if __name__ == "__main__":
    main()