# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import TypedDict


import pygame


class Change:
    class LayersGroup(TypedDict):
        surface: pygame.Surface
        pos: tuple[int, int]

    @staticmethod
    def layers(
        surface: pygame.Surface,
        group: tuple[tuple[LayersGroup]],
        timer: int,
        interval: tuple[int, ...],
        shortly: bool,
        color: tuple[int, int, int, int] = (0, 0, 0, 0)
    ) -> pygame.Surface:
        if shortly:
            surface.fill(color)
            for i in range(len(group)):
                for j in group[i]:
                    surface.blit(j["surface"], j["pos"])
        else:
            for i in range(len(group)):
                if timer == interval[i]:
                    for j in group[i]:
                        surface.blit(j["surface"], j["pos"])

        return surface


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