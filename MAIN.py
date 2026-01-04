import sys

import pygame


def main():
    pygame.display.init()
    pygame.font.init()

    pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')

    import SCRIPT.KERNEL as _


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    main()