# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import sys


def main():
    project = '点线 Project'
    title = '锐行 ~ Thunder Out of the Mountain'
    version = '1.2'
    author = 'An_172N'

    sys.dont_write_bytecode = True
    for module in ('numpy', 'timidity', 'pygame.examples'):
        sys.modules[module] = None

    import pygame

    clock = pygame.time.Clock()

    pygame.display.init()
    pygame.display.set_caption(title)
    pygame.font.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)

    import SCRIPT.KERNEL

    print(f"{project} | {title} | Ver {version} | By {author}")
    SCRIPT.KERNEL.update(clock, version, title)


if __name__ == "__main__":
    main()