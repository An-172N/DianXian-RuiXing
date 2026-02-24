# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import pygame as pg


from PRELOAD import item_cache, particle_cache
from LOGIC.SPRITE import Base


class Item(Base):
    __slots__ = ('speed')

    def __init__(th, type: str, speed: float, pos: tuple, *group: pg.sprite.Group, size: tuple=(0, 0), color: tuple=(0, 0, 0)):
        super().__init__(type, item_cache[type] if type != "char" else particle_cache[(size, color)], *group, pos=pos)

        th.speed = speed
    
    def update(th):
        th.y -= th.speed

        if th.type in ["power", "flash"]:
            th.speed -= 0.1

            if th.speed < -2:
                th.speed = -2
        elif th.type == "char":
            th.speed -= 0.1
            if th.speed < -4:
                th.speed = -4

        if th.y >= 360:
            th.kill()