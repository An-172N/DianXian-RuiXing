# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


def main():
    project = '点线 Project'
    title = '锐行 ~ Thunder Out of the Mountain'
    version = '1.1.0'
    author = 'An_172N'

    import sys

    sys.dont_write_bytecode = True
    for module in ('numpy', 'timidity', 'pygame.examples'):
        sys.modules[module] = None

    import argparse

    parser = argparse.ArgumentParser()
    for i, j in (('-stage', 1), ('-level', 1), ('-flash', 3), ('-power', 0), ('-seed', None)):
        parser.add_argument(i, type=int, default=j)
    args = parser.parse_args()
    args_tuple = (int(args.stage), int(args.level), int(args.flash), int(args.power))

    import random

    random.seed(args.seed)

    import pygame

    clock = pygame.time.Clock()

    pygame.display.init()
    pygame.display.set_caption(title)
    pygame.font.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((480, 360), pygame.FULLSCREEN|pygame.SCALED, vsync=1)

    import SCRIPT

    print(f"{project} | {title} | Ver {version} | By {author}")
    SCRIPT.KERNEL.update(clock, screen, args_tuple, version)


if __name__ == "__main__":
    main()