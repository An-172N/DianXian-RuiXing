# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, sample, random
from math import radians, sin, cos


import pygame as pg


from PRELOAD import *
from LOGIC.CALCULATE import *
from LOGIC.SPRITE import *


class Barrage(Base):
    def __init__(th, effective: pg.Rect, form: str, speed: float, color: tuple, angle: float, pos: tuple, image: pg.Surface, group: pg.sprite.Group, mask: bool=True, rotate: bool=True):
        super().__init__(form, image, group, angle=angle, pos=pos, mask=mask, rotate=rotate)

        th.effective = effective
        th.speed = speed
        th.color = color

    def update(th):
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


class Text(Base):
    def __init__(th, pos: tuple, kill_time: tuple, speed: float, image: pg.Surface, target_image: pg.Surface, group: pg.sprite.Group):
        super().__init__(None, image, group, pos=pos)

        th.target_image = target_image
        th.kill_time = kill_time
        th.speed = speed
        th.timer = 0

        sound_cache["charge"].play(maxtime=128)

    def update(th):
        th.timer += 1
        th.y -= th.speed

        if th.timer >= th.kill_time[1]:
            th.kill()
        elif th.timer >= th.kill_time[0] and th.image != th.target_image:
            th.image = th.target_image


class Rect(Base):
    def __init__(th, image: pg.Surface, *group: pg.sprite.Group, pos: tuple=(0, 0), mask: bool=False):
        super().__init__(None, image, *group, pos=pos, mask=mask)


class Brick(Base):
    def __init__(th, form: str, hp: int, color: tuple, pos: tuple, image: pg.Surface, group: pg.sprite.Group):
        super().__init__(form, image, group, pos=pos)

        th.color = color
        th.hp = hp
        th.power = False
        th.flash = False
        th.is_die = False


class Bullet(Base):
    def __init__(th, effective: pg.Rect, form: str, speed: float, color: tuple, angle: float, pos: tuple, damage: int, image: pg.Surface, group: pg.sprite.Group, mask: bool=True, rotate: bool=True):
        super().__init__(form, image, group, angle=angle, pos=pos, mask=mask, rotate=rotate)

        th.effective = effective
        th.speed = speed
        th.color = color
        th.damage = damage

    def update(th):
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


class Item(Base):
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


class Line(Base):
    def __init__(th, size: tuple, damage: int, angle: float, pos: tuple, color: tuple, target_color: tuple, group: pg.sprite.Group, mask: bool):
        super().__init__("line", line_cache[(size[1], angle, color)], group, angle=angle, pos=pos, mask=mask)

        th.size = size
        th.damage = damage
        th.color = color
        th.target_color = target_color
        th.timer = 0

    def update(th):
        th.timer += 1

        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            th.color = th.target_color
            th.image = line_cache[(th.size[1], th.angle, th.color)]


def line_barrage(color: list, locate: tuple, group: pg.sprite.Group):
    start_pos = (randint(120, 465), 15)
    end_pos = (-locate[0], -locate[1])
    delta_pos = add(end_pos, start_pos)
    pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
    angle = approximate(bearing(-delta_pos[0], -delta_pos[1]))

    Line((3, 500), 0, angle, pos, color[1], color[2], group, True)


def line_brick(group: pg.sprite.Group, spawn_pos: tuple):
    for _ in range(12):
        angle = approximate(randint(0, 360))

        Line((2, choice([48, 96, 192])), 6, angle, spawn_pos, color_dict[5], color_dict[9], group, False)


def circle_brick(group: pg.sprite.Group, spawn_pos: tuple):
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        Bullet(effective, "bullet", 16, 0, i, spawn_pos, 4, bullet_cache["bullet"], group, False).update()


def polygon_brick(group: pg.sprite.Group, *spawn_pos: tuple):
    bullet_index = [
        {
            'angle': choice([-30, -210]),
            'pos': spawn_pos[0]
        },
        {
            'angle': choice([30, 210]),
            'pos': spawn_pos[1]
        },
        {
            'angle': choice([90, 270]),
            'pos': spawn_pos[2]
        }
    ]

    for bullet_info in bullet_index:
        Bullet(effective, "bullet-cross", 16, 0, bullet_info['angle'], bullet_info['pos'], 4, bullet_cache["bullet-cross"], group, False)


def point_brick(group: pg.sprite.Group):
    for _ in range(24):
        pos = (randint(120, 465), randint(15, 345))
        angle = randint(0, 360)

        Bullet(effective, "bullet", 16, 0, angle, pos, 4, bullet_cache["bullet"], group, False)


def load_brick(row: int, line: str, color: tuple, hp: int, rate: float, size: tuple, interval: tuple, group: pg.sprite.Group):
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if random() >= rate else color_dict[6]

            Brick(shape, hp, c, (size[0] + i * interval[0], size[1] + row * interval[1]), brick_cache[(shape, c)], group)


def choose_brick(group: pg.sprite.Group, numbers: tuple, basic_power: int, basic_flash: int):
    brick_list = list(group)
    choose_power = sample(range(len(brick_list)), basic_power + numbers[0] + numbers[1])
    choose_flash = sample(range(len(brick_list)), basic_flash)

    for i in choose_power:
        brick_list[i].power = True
    for j in choose_flash:
        brick_list[j].flash = True


def circle_barrage(type: int, color: list, spawn_pos: tuple, locate: tuple, group: pg.sprite.Group):
    two_point = add(locate, (-spawn_pos[0], -spawn_pos[1]))
    angle = bearing(-two_point[0], -two_point[1])

    Barrage(effective, type, 3, color[0], angle, spawn_pos, barrage_cache[(type, color[0])], group, rotate=False)


def polygon_barrage(type: int, color: list, spawn_pos: tuple, locate: tuple, group: pg.sprite.Group):
    for i in range(locate[0] - 32, locate[0] + 33, 64):
        two_point = add((i, locate[1]), (-spawn_pos[0], -spawn_pos[1]))
        angle = bearing(-two_point[0], -two_point[1])

        Barrage(effective, type, 3, color[0], angle, spawn_pos, barrage_cache[(type, color[0])], group)


def point_barrage(type: int, color: list, locate: tuple, group: pg.sprite.Group):
    for _ in range(3):
        pos = (randint(120, 465), randint(15, 225))
        two_point = add(locate, (-pos[0], -pos[1]))
        angle = bearing(-two_point[0], -two_point[1])

        Barrage(effective, type, 4, color[0], angle, pos, barrage_cache[(type, color[0])], group, rotate=False)


def spawn_particles(group: pg.sprite.Group, size: tuple, pos: tuple, speed: tuple, color1: tuple, color2: tuple=None):
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else choice([color1, color2])

        Barrage(effective, None, randint(speed[0], speed[1]), color, i, pos, particle_cache[(size, color)], group, False, False)