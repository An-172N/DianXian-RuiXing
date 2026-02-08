# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import os

import pygame

from SOURCE import LOGIC


asset = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\ASSET')
font = pygame.font.Font(os.path.join(asset, 'FONT\FONT_UNIFONT.otf'), 15)
icon = pygame.display.set_icon(pygame.image.load(os.path.join(asset, '..\ICON.ico')))


char_image = pygame.image.load(os.path.join(asset, 'IMAGE\IMG_CHAR.png')).convert_alpha()
brick_image = pygame.image.load(os.path.join(asset, 'IMAGE\IMG_BRICK.png')).convert_alpha()
barrage_image = pygame.image.load(os.path.join(asset, 'IMAGE\IMG_BARRAGE.png')).convert_alpha()
picture = {
    1: pygame.image.load(os.path.join(asset, 'IMAGE\IMG_STAGE1BG.png')).convert(),
    2: pygame.image.load(os.path.join(asset, 'IMAGE\IMG_STAGE2BG.png')).convert(),
    3: pygame.image.load(os.path.join(asset, 'IMAGE\IMG_STAGE3BG.png')).convert(),
    4: pygame.image.load(os.path.join(asset, 'IMAGE\IMG_STAGE4BG.png')).convert(),
    5: LOGIC.Tool.draw_rectangle((345, 330), 0, (0, 0, 0)).convert(),
    6: pygame.image.load(os.path.join(asset, 'IMAGE\IMG_GAMEBG.png')).convert_alpha()
}


color_dict = {
    1: (255, 128, 0),
    2: (0, 255, 0),
    3: (128, 0, 128),
    4: (251, 234, 18),
    5: (45, 194, 229)
}


barrage_rate = [0.17 + (LOGIC.FUNC.fibonacci(0, 1, i) / 100) for i in range(4, 8)]