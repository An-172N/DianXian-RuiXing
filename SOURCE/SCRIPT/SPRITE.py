# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, sample, random
from math import radians, sin, cos


import pygame as pg


from PRELOAD import *
from LOGIC.CALCULATE import *
from LOGIC.SPRITE import *


class Barrage(Base):
    def __init__(th, effective: pg.Rect, form: str, speed: float, color: tuple, angle: float, pos: tuple, damage: int, image: pg.Surface, group: pg.sprite.Group, rotate: bool=True, radius: int=0):
        super().__init__(image, group, form=form, angle=angle, pos=pos, rotate=rotate, radius=radius)

        th.effective = effective
        th.speed = speed
        th.color = color
        if damage:
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
    def __init__(th, pos: tuple, kill_time: tuple, speed: float, text: str, color: tuple, target_color: tuple, group: pg.sprite.Group):
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


class Rect(Base):
    def __init__(th, image: pg.Surface, *group: pg.sprite.Group, pos: tuple=(0, 0), radius: int=0):
        super().__init__(image, *group, pos=pos, radius=radius)


class Brick(Base):
    def __init__(th, form: str, hp: int, color: tuple, pos: tuple, image: pg.Surface, group: pg.sprite.Group):
        super().__init__(image, group, form=form, pos=pos, mask=True)

        th.color = color
        th.hp = hp
        th.power = False
        th.flash = False
        th.is_die = False


class Item(Base):
    def __init__(th, type: str, speed: float, pos: tuple, *group: pg.sprite.Group):
        super().__init__(item_cache[type], *group, form=type, pos=pos)

        th.speed = speed

    def update(th):
        th.y -= th.speed

        if th.type in ("power", "flash"):
            th.speed -= 0.1

            if th.speed < -2:
                th.speed = -2
        if th.y >= 360:
            th.kill()


class Line(Base):
    def __init__(th, color: tuple, target_color: tuple, damage: int, pos: tuple, image: pg.Surface, target_image: pg.Surface, group: pg.sprite.Group, mask: bool=False):
        super().__init__(image, group, form="line", pos=pos, mask=mask)

        th.color = color
        th.target_color = target_color
        if damage:
            th.damage = damage
        th.target_image = target_image
        th.timer = 0

    def update(th):
        th.timer += 1

        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.image != th.target_image:
            th.color = th.target_color
            th.image = th.target_image


def line_brick(group: pg.sprite.Group, spawn_pos: tuple):
    for _ in range(12):
        angle = approximate(randint(0, 360))
        rands = choice([64, 128, 192])
        
        Line(color_dict[5], color_dict[9], 6, spawn_pos, line_cache[(rands, angle, color_dict[5])], line_cache[(rands, angle, color_dict[9])], group, True)


def circle_brick(group: pg.sprite.Group, spawn_pos: tuple, delay: int):
    for i in range(0 + delay, 360 + delay, 15):
        Barrage(effective, "bullet", 16, 0, i, spawn_pos, 4, bullet_cache["bullet"], group).update()


def polygon_brick(group: pg.sprite.Group, *spawn_pos: tuple):
    bullet_index = (
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
    )

    for info in bullet_index:
        Barrage(effective, "bullet-cross", 16, 0, info['angle'], info['pos'], 4, bullet_cache["bullet-cross"], group)


def point_brick(group: pg.sprite.Group):
    for _ in range(24):
        Barrage(effective, "bullet", 16, 0, randint(0, 360), (randint(120, 465), randint(15, 345)), 4, bullet_cache["bullet"], group)


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
    delta = add(locate, (-spawn_pos[0], -spawn_pos[1]))

    Barrage(effective, type, 3, color[0], direct(-delta[0], -delta[1]), spawn_pos, 0, barrage_cache[(type, color[0])], group, False, 3)


def polygon_barrage(type: int, color: list, spawn_pos: tuple, locate: tuple, group: pg.sprite.Group):
    for i in range(locate[0] - 32, locate[0] + 33, 64):
        delta = add((i, locate[1]), (-spawn_pos[0], -spawn_pos[1]))

        Barrage(effective, type, 3, color[0], direct(-delta[0], -delta[1]), spawn_pos, 0, barrage_cache[(type, color[0])], group, radius=1.5)


def line_barrage(color: list, current: tuple, target: tuple, group: pg.sprite.Group):
    while True:
        if not effective.collidepoint(current):
            break

        Line(color[1], color[2], 0, current, particle_cache[(3, color[1])], particle_cache[(3, color[2])], group)

        if math.dist(current, target) < 1e-6:
            break

        current = vector(current, target, 3)[0]


def point_barrage(type: int, color: list, locate: tuple, group: pg.sprite.Group):
    for _ in range(3):
        pos = (randint(120, 465), randint(15, 225))
        delta = add(locate, (-pos[0], -pos[1]))

        Barrage(effective, type, 4, color[0], direct(-delta[0], -delta[1]), pos, 0, barrage_cache[(type, color[0])], group, False, 3)


def spawn_particles(group: pg.sprite.Group, size: int, pos: tuple, speed: tuple, color1: tuple, color2: tuple=None):
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else choice([color1, color2])

        Barrage(effective, None, randint(speed[0], speed[1]), color, i, pos, 0, particle_cache[(size, color)], group, False)