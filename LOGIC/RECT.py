# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


class Rect(pygame.sprite.Sprite):
    def __init__(th, size: tuple, border: float, color: tuple, pos: tuple=(0, 0)):
        super().__init__()

        th.width = size[0]
        th.height = size[1]
        th.border = border
        th.color = color

        th.image = th.get_surface()
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos

    def get_surface(th) -> pygame.Surface:
        surface = pygame.Surface((th.width, th.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, th.color, surface.get_rect(), th.border)
            
        return surface