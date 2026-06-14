# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import sys
import argparse
import random


def main():
    project = '点线 Project'
    title = '锐行 ~ Thunder Out of the Mountain'
    version = '1.2'
    author = 'An_172N'
    sys.dont_write_bytecode = True
    for module in ('numpy', 'timidity', 'pygame.examples'):
        sys.modules[module] = None
    parser = argparse.ArgumentParser()
    for i, j in (('-s', 1), ('-l', 1), ('-f', 3), ('-p', 0), ('-sd', None)):
        parser.add_argument(i, type=int, default=j)
    args = parser.parse_args()
    args_tuple = (int(args.s), int(args.l), int(args.f), int(args.p))
    random.seed(args.sd)

    import pygame

    clock = pygame.time.Clock()
    pygame.display.init()
    pygame.display.set_caption(title)
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)

    import SCRIPT.KERNEL

    print(f"{project} | {title} | Ver {version} | By {author}")
    SCRIPT.KERNEL.update(clock, args_tuple, version, title)


if __name__ == "__main__":
    main()