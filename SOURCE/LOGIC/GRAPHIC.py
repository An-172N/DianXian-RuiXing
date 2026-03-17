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

    @staticmethod
    def color(
        surface: pygame.Surface,
        color: tuple[int, int, int]
    ) -> pygame.Surface:
        width, height = surface.get_size()

        for x in range(width):
            for y in range(height):
                alpha = surface.get_at((x, y))[3]

                surface.set_at((x, y), (*color, alpha))

        return surface


class Draw:
    @staticmethod
    def rectangle(
        size: tuple[int | float, int | float],
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
        xy_size: tuple[int | float, int | float, int | float, int | float],
        border: int | float,
        color: tuple[int, int, int]
    ) -> pygame.Surface:
        return (
            surface := pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA),
            pygame.draw.ellipse(surface, color, xy_size, border)
        )[0]
    

class FPSGetter:
    def __init__(th,
        clock: pygame.time.Clock,
        interval: int = 500,
        bit: int = 0
    ) -> None:
        th.clock = clock
        th.interval = interval
        th.bit = bit

        th._last_time = pygame.time.get_ticks()
        th._fps = f"{th._last_time}"

    @property
    def fps(th) -> str:
        return th._fps

    def update(th) -> None:
        current_time = pygame.time.get_ticks()

        if current_time - th._last_time >= th.interval:
            th._fps = f"{th.clock.get_fps():.{th.bit}f}"
            th._last_time = current_time