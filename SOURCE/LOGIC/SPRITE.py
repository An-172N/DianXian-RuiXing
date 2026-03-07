# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any


import pygame


class Base(pygame.sprite.Sprite):
    def __init__(th,
        form: int | str,
        image: pygame.Surface,
        *group: pygame.sprite.Group,
        angle: int | float = 0,
        pos: tuple[int, int] = (0, 0),
        mask: bool = False,
        rotate: bool = False
    ) -> None:
        super().__init__(*group)

        th.image = pygame.transform.rotate(image, angle) if rotate else image
        th.rect = th.image.get_rect(center=pos)
        th.angle = angle
        th._x, th._y = pos
        if mask:
            th.mask = pygame.mask.from_surface(th.image)
        if form is not None:
            th.type = form

    @property
    def x(th) -> int | float:
        return th._x

    @x.setter
    def x(th,
        value: int | float
    ) -> None:
        th._x = value
        th.rect.centerx = th._x

    @property
    def y(th) -> int | float:
        return th._y

    @y.setter
    def y(th,
        value: int | float
    ) -> None:
        th._y = value
        th.rect.centery = th._y


def spawn_sprite(
    condition: bool,
    sprite: Callable[..., Any],
    *args: Any,
    group: pygame.sprite.Group = None,
    timer: int = 0
) -> int:
    timer += 1

    if condition:
        char = sprite(*args)

        if group is not None:
            group.add(char)

        timer = 0

    return timer


def vector(
    present: tuple[int | float, int | float],
    target: tuple[int | float, int | float],
    speed: int | float
) -> tuple[pygame.Vector2, pygame.Vector2]:
    dir = pygame.math.Vector2(target[0] - present[0], target[1] - present[1])
    current = pygame.math.Vector2(present[0], present[1])
    target = pygame.math.Vector2(target[0], target[1])

    delta_vec = target - current
    distance = delta_vec.length()

    if distance < speed:
        return target, delta_vec
    else:
        if distance > 0:
            dir.normalize_ip()

        return current + dir * speed, delta_vec