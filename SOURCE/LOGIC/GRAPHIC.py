# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any, TypedDict


import pygame


class PopDict(TypedDict):
    text: str
    pos: tuple[int, int]
    color: tuple[int, int, int]


def pop(
    surface: pygame.Surface,
    font: pygame.font.Font,
    group: tuple[list[PopDict], list[PopDict], list[PopDict]],
    timer: int,
    interval: tuple[int, int, int],
    play: Callable[..., Any],
    *args: Any
) -> tuple[pygame.Surface, int]:
    def blit_text(
        timer: int,
        interval: int,
        gather: list[PopDict],
        surface: pygame.Surface,
        font: pygame.font.Font
    ) -> None:
        if timer >= interval:
            for i in gather:
                color = i["color"] if "color" in i else (255, 255, 255)
                text = font.render(i["text"], False, color).convert_alpha()

                surface.blit(text, i["pos"])

    for i in range(0, 3):
        blit_text(timer, interval[i], group[i], surface, font)

    if timer < interval[2]:
        timer += 1

        if timer == interval[2]:
            play(*args)

    return surface, timer


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