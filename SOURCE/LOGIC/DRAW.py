# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


def rectangle(size: tuple, border: float, color: tuple) -> pygame.Surface:
    surface = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)

    pygame.draw.rect(surface, color, surface.get_rect(), border)

    return surface


def circle(xy_size: tuple, border: float, color: tuple) -> pygame.Surface:
    surface = pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA)

    pygame.draw.ellipse(surface, color, xy_size, border)

    return surface