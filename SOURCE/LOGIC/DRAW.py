# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any, TypedDict


import pygame


class PopGroup(TypedDict):
    text: str
    pos: tuple[int, int]


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


def pop_animate(
    surface: pygame.Surface,
    font: pygame.font.Font,
    group: tuple[list[PopGroup], list[PopGroup], list[PopGroup]],
    timer: int,
    interval: tuple[int, int, int],
    play: Callable[..., Any],
    *args: Any,
    color: tuple[int, int, int] = (255, 255, 255)
) -> tuple[pygame.Surface, int]:
    def blit_text(
        timer: int,
        interval: int,
        gather: list[PopGroup]
    ) -> None:
        if timer >= interval:
            for i in gather:
                text = font.render(i["text"], False, color).convert_alpha()

                surface.blit(text, i["pos"])

    blit_text(timer, interval[0], group[0])
    blit_text(timer, interval[1], group[1])
    blit_text(timer, interval[2], group[2])

    if timer < interval[2]:
        timer += 1

        if timer == interval[2]:
            play(*args)

    return surface, timer