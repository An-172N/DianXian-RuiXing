# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame


class Change:
    @staticmethod
    def swivel(
        original_image: pygame.Surface,
        turn_image: pygame.Surface,
        flip: bool,
        turn: bool
    ) -> pygame.Surface:
        if flip:
            return pygame.transform.flip(turn_image, True, False)
        elif turn:
            return turn_image
        else:
            return original_image


class Draw:
    @staticmethod
    def rectangle(
        size: tuple[float, float],
        border: int | float,
        color: tuple[int, int, int],
        radius: tuple[int, int, int, int] = (-1, -1, -1, -1)
    ) -> pygame.Surface:
        return (
            surface := pygame.Surface(size, pygame.SRCALPHA),
            pygame.draw.rect(surface, color, surface.get_rect(), border, -1, *radius)
        )[0]

    @staticmethod
    def circle(
        xy_size: tuple[float, float, float, float],
        border: float,
        color: tuple[int, int, int]
    ) -> pygame.Surface:
        return (
            surface := pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA),
            pygame.draw.ellipse(surface, color, xy_size, border)
        )[0]