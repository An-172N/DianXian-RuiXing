# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from typing import Callable, Any


import pygame


class Base(pygame.sprite.Sprite):
    def __init__(th,
        original_image: pygame.Surface,
        *group: pygame.sprite.Group,
        turn_image: pygame.Surface = None,
        form: int | str = None,
        angle: float = 0,
        pos: tuple[int, int] = (0, 0),
        mask: bool = False,
        radius: float = None,
        rotate: bool = False
    ) -> None:
        super().__init__(*group)

        th.original_image = original_image
        th.turn_image = turn_image
        if turn_image is not None:
            th.turn_image_flipped = pygame.transform.flip(turn_image, True, False)
        th.image = th.original_image if not rotate else pygame.transform.rotate(th.original_image, angle)
        th.rect = th.image.get_rect(center=pos)
        th.angle = angle
        if radius:
            th.radius = radius
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

    def swivel(th,
        flip: bool,
        turn: bool
    ) -> None:
        if flip:
            th.image = th.turn_image_flipped
        elif turn:
            th.image = th.turn_image
        else:
            th.image = th.original_image


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


def bomb(
    condition: bool,
    power: int,
    critical: int
) -> tuple[bool, int]:
    if not condition and power >= critical:
        condition = True
        power -= critical

    return condition, power


def collide(
    sprite1: pygame.sprite.Sprite,
    sprite2: pygame.sprite.Sprite
) -> tuple[int, int] | bool | None:
    if hasattr(sprite1, 'mask') and hasattr(sprite2, 'mask'):
        return pygame.sprite.collide_mask(sprite1, sprite2)
    elif hasattr(sprite1, 'radius') and hasattr(sprite2, 'radius'):
        return pygame.sprite.collide_circle(sprite1, sprite2)
    else:
        return pygame.sprite.collide_rect(sprite1, sprite2)