# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame as pg


from LOGIC.SPRITE import Base


class Basic(Base):
    __slots__ = ('group', 'particle_group', 'locate', 'hp', 'color', 'is_die', 'can_shoot', 'point', 'choice', 'timer', 'torrent', 'target_pos', '_x', '_y')

    def __init__(th, image: pg.Surface, locate: tuple, hp: int, color: tuple, *group: pg.sprite.Group):
        super().__init__(None, image, pos=(292, 60))

        th.group = group[0]
        th.particle_group = group[1]
        th.locate = locate
        th.hp = hp
        th.color = color
        th.is_die = False
        th.can_shoot = False
        th.point = None
        th.choice = None
        th.timer = 0
        th.torrent = 0
        th.target_pos = (292, 60)
        th._x, th._y = th.rect.center

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