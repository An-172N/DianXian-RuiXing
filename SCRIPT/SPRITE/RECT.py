# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

from LOGIC import Tool


class Rect(pygame.sprite.Sprite):
    def __init__(th, size: tuple, border: float, color: tuple, pos: tuple=(0, 0)):
        super().__init__()

        th.image =Tool.draw_rectangle((size[0], size[1]), border, color).convert()
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos