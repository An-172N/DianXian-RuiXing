# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame


def rectangle(
    size: tuple[int | float, int | float],
    border: float,
    color: tuple[int, int, int]
) -> pygame.Surface:
    surface = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)

    pygame.draw.rect(surface, color, surface.get_rect(), border)

    return surface


def circle(
    xy_size: tuple[int | float, int | float, int | float, int | float],
    border: float,
    color: tuple[int, int, int]
) -> pygame.Surface:
    surface = pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA)

    pygame.draw.ellipse(surface, color, xy_size, border)

    return surface