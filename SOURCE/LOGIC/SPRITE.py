# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame


class Base(pygame.sprite.Sprite):
    def __init__(th, form: object, image: pygame.Surface, *group: pygame.sprite.Group, angle: float=0, pos: tuple=(0, 0), mask: bool=False, rotate: bool=False):
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
    def x(th):
        return th._x

    @x.setter
    def x(th, value):
        th._x = value
        th.rect.centerx = th._x

    @property
    def y(th):
        return th._y

    @y.setter
    def y(th, value):
        th._y = value
        th.rect.centery = th._y