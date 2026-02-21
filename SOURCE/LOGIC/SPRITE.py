# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


class Base(pygame.sprite.Sprite):
    __slots__ = ('angle', 'type', 'image', 'rect', 'mask', '_x', '_y')

    def __init__(th, form: object, image: pygame.Surface, angle: float=0, pos: tuple=(0, 0), mask: bool=False, rotate: bool=False):
        super().__init__()

        th.type = form
        th.angle = angle
        th.image = pygame.transform.rotate(image, angle) if rotate else image
        th.rect = th.image.get_rect(center=pos)
        if mask:
            th.mask = pygame.mask.from_surface(th.image)
        th._x, th._y = pos

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