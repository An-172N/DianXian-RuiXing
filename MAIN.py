# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import sys


def main() -> int:
    import pygame

    clock = pygame.time.Clock()

    pygame.display.init()
    pygame.display.set_caption('锐行 ~ Thunder Out of the Mountain')
    pygame.font.init()

    screen = pygame.display.set_mode((480, 360), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.FULLSCREEN|pygame.SCALED, vsync=1)

    import SCRIPT

    SCRIPT.update(clock, screen)

    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    
    block_module = [
        'numpy', 'timidity',
        'pygame._freetype', 'pygame._sdl2', 'pygame._camera',
        'pygame._camera_vidcapture', 'pygame._sprite', 'pygame._camera_opencv',
        'pygame.mixer_music', 'pygame.mixer', 'pygame.joystick',
        'pygame.gfxdraw', 'pygame.mouse', 'pygame.threads',
        'pygame.pypm', 'pygame.macosx', 'pygame.examples',
        'pygame.locals', 'pygame.camera', 'pygame.__pyinstaller',
        'pygame.freetype', 'pygame.midi', 'pygame.scrap',
        'pygame.pixelarray', 'pygame.pixelcopy', 'pygame.newbuffer',
        'pygame.ftfont', 'pygame.fastevent', 'pygame.sndarray',
        'pygame.surfarray', 'pygame.cursors', 'pygame.pkgdata',
        'pygame.draw_py'
    ]

    for module in block_module:
        sys.modules[module] = None

    main()