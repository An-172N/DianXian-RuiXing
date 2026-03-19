# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any


import pygame


class Base(pygame.sprite.Sprite):
    def __init__(th,
        image: pygame.Surface,
        *group: pygame.sprite.Group,
        form: int | str = None,
        angle: float = 0,
        pos: tuple[int, int] = (0, 0),
        mask: bool = False,
        rotate: bool = False
    ) -> None:
        super().__init__(*group)

        th.image = pygame.transform.rotate(image, angle) if rotate else image
        th.rect = th.image.get_rect(center=pos)
        th.angle = angle
        if mask:
            th.mask = pygame.mask.from_surface(th.image)
        if form is not None:
            th.type = form

        th._x, th._y = pos

    @property
    def x(th) -> float:
        return th._x

    @x.setter
    def x(th,
        value: float
    ) -> None:
        th._x = value
        th.rect.centerx = th._x

    @property
    def y(th) -> float:
        return th._y

    @y.setter
    def y(th,
        value: float
    ) -> None:
        th._y = value
        th.rect.centery = th._y


class Invinc:
    def __init__(th,
        end: int,
        blink_interval: int,
        func: Callable[..., Any] = lambda: None,
        *func_args: Any
    ) -> None:
        th.end = end
        th.blink_interval = blink_interval
        th.func = func
        th.func_args = func_args

        th._condition = False
        th._visitable = True
        th._timer = 0

    @property
    def condition(th) -> bool:
        return th._condition

    @condition.setter
    def condition(th,
        value: bool
    ) -> None:
        th._condition = value

    @property
    def visitable(th) -> bool:
        return th._visitable

    def update(th) -> None:
        if th._condition:
            th._timer += 1

            if th._timer >= th.end:
                th.func(*th.func_args)

                th._timer = 0
                th._visitable = True
                th._condition = False
            else:
                th._visitable = (th._timer // th.blink_interval) % 2 == 1


def move(
    value: float,
    speed: tuple[float, float],
    forward: bool,
    backward: bool,
    change: bool
) -> int | float:
    if forward:
        value -= speed[1] if change else speed[0]
    if backward:
        value += speed[1] if change else speed[0]

    return value


def bomb(
    condition: bool,
    power: int,
    critical: int
) -> tuple[bool, int]:
    if not condition and power >= critical:
        condition = True
        power -= critical

    return condition, power