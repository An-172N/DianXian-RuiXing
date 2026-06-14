# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from math import radians, sin, cos


import pygame as pg
from pygame.sprite import Group


from PRELOAD import *
from LOGIC.CALCULATE import *
from LOGIC.SPRITE import *


class Barrage(Base):
    def __init__(th, effective: pg.Rect, speed: float, angle: float, pos: tuple, image: pg.Surface, group: Group, radius: int=0, form: str=None, rotate: bool=False):
        super().__init__(image, group, None, form, angle, pos, radius=radius, rotate=rotate)
        th.effective = effective
        th.speed = speed

    def update(th):
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)
        if hasattr(th, "type") and th.type == "char":
            th.speed -= 0.1
            if th.speed < -4:
                th.speed = -4
        if not th.effective.collidepoint(th.rect.center):
            th.kill()


class Bullet(Base):
    def __init__(th, effective: pg.Rect, speed: float, angle: float, pos: tuple, damage: int, image: pg.Surface, group: Group, form: str=None, rotate: bool=False):
        super().__init__(image, group, None, form, angle, pos, rotate=rotate)
        th.effective = effective
        th.speed = speed
        th.damage = damage

    def update(th):
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)
        if hasattr(th, "type") and th.type == "char":
            th.speed -= 0.1
            if th.speed < -4:
                th.speed = -4
        if not th.effective.collidepoint(th.rect.center):
            th.kill()


class Text(Base):
    def __init__(th, pos: tuple, kill_time: tuple, speed: float, text: str, color: tuple, target_color: tuple, group: Group):
        super().__init__(font.render(text, False, color), group, pos=pos)
        th.text = text
        th.color = color
        th.target_color = target_color
        th.kill_time = kill_time
        th.speed = speed
        th.timer = 0
        sound_cache["charge"].play(maxtime=128)

    def update(th):
        th.timer += 1
        th.y -= th.speed
        if th.timer >= th.kill_time[1]:
            th.kill()
        elif th.timer >= th.kill_time[0] and th.color != th.target_color:
            th.color = th.target_color
            th.image = font.render(th.text, False, th.color)


class Brick(Base):
    def __init__(th, form: str, hp: int, color: tuple, pos: tuple, image: pg.Surface):
        super().__init__(image, form=form, pos=pos, mask=True)
        th.color = color
        th.hp = hp
        th.power = False
        th.flash = False
        th.is_die = False


class Item(Base):
    def __init__(th, type: str, speed: float, pos: tuple, group: Group):
        super().__init__(item_cache[type], group, form=type, pos=pos)
        th.speed = speed

    def update(th):
        th.y -= th.speed
        th.speed -= 0.1
        if th.speed < -2:
            th.speed = -2
        if th.y >= 360:
            th.kill()


class Line(Base):
    def __init__(th, color: tuple, target_color: tuple, damage: int, pos: tuple, target: tuple, count: int, image: pg.Surface, group: Group):
        super().__init__(image, group, form="line", pos=pos, radius=1.5)
        th.color = color
        th.target_color = target_color
        th.pos = pos
        th.count = count
        if not count:
            th.target = target
        if damage:
            th.damage = damage
        th.timer = 0

    def draw_line(th):
        if not th.count:
            pg.draw.line(screen, th.color, th.pos, th.target, 3)

    def update(th):
        th.timer += 1
        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45:
            if th.color != th.target_color:
                th.color = th.target_color


class LineBullet(Base):
    def __init__(th, damage: int, pos: tuple, image: pg.Surface, target_image: pg.Surface, group: Group):
        super().__init__(image, group, form="line", pos=pos, mask=True)
        th.damage = damage
        th.target_image = target_image
        th.timer = 0

    def update(th):
        th.timer += 1
        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.image != th.target_image:
            th.image = th.target_image