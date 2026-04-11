# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, sample, uniform


from PRELOAD import *
from LOGIC.CALCULATE import *
from SCRIPT.SPRITE import *


def line_brick(group: pg.sprite.Group, spawn_pos: tuple):
    for _ in range(12):
        angle = approximate(randint(0, 360))
        rands = choice([48, 96, 160])
        image, target_image = [line_cache[(rands, angle, color_dict[i])] for i in (5, 9)]
        Line(color_dict[5], color_dict[9], 6, spawn_pos, image, target_image, group, True)


def circle_brick(group: pg.sprite.Group, spawn_pos: tuple):
    image = bullet_cache["bullet"]
    delay = randint(0, 12)
    for i in range(0 + delay, 360 + delay, 12):
        Barrage(effective, 16, 0, i, spawn_pos, 4, image, group, form="bullet", rotate=True).update()


def polygon_brick(group: pg.sprite.Group, *spawn_pos: tuple):
    image = bullet_cache["bullet"]
    for i, angle in enumerate(range(-30, 91, 60)):
        for j in (0, 1):
            if angle in (30, -30) and j:
                Barrage(effective, 16, 0, angle, spawn_pos[i], 4, image, group, form="bullet-cross", rotate=True)
            elif angle == 90:
                angle = angle + j * 180
                Barrage(effective, 16, 0, angle, spawn_pos[i], 4, image, group, form="bullet-cross", rotate=True)


def point_brick(group: pg.sprite.Group):
    image = bullet_cache["bullet"]
    for _ in range(24):
        pos = (randint(120, 465), randint(15, 320))
        angle = randint(0, 360)
        Barrage(effective, 16, 0, angle, pos, 4, image, group, form="bullet", rotate=True)


def load_brick(row: int, line: str, color: tuple, hp: int, rate: float, size: tuple, interval: tuple):
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if uniform(0, 1) >= rate else color_dict[6]
            pos = (size[0] + i * interval[0], size[1] + row * interval[1])
            image = brick_cache[(shape, c)]
            brick_ready.append(Brick(shape, hp, c, pos, image))


def choose_brick(group: list, numbers: tuple, basic_power: int, basic_flash: int):
    choose_power = sample(range(len(group)), basic_power + numbers[0] + numbers[1])
    choose_flash = sample(range(len(group)), basic_flash)
    for i in choose_power:
        group[i].power = True
    for i in choose_flash:
        group[i].flash = True


def circle_barrage(type: int, color: tuple, spawn_pos: tuple, locate: tuple, group: pg.sprite.Group):
    delta = add(locate, inverse(spawn_pos))
    angle = direct(*inverse(delta))
    image = barrage_cache[(type, color)]
    Barrage(effective, 3, color, angle, spawn_pos, 0, image, group, 3)


def polygon_barrage(type: int, color: tuple, spawn_pos: tuple, locate: tuple, group: pg.sprite.Group):
    image = barrage_cache[(type, color)]
    for i in range(locate[0] - 32, locate[0] + 33, 64):
        delta = add((i, locate[1]), inverse(spawn_pos))
        angle = direct(*inverse(delta))
        Barrage(effective, 3, color, angle, spawn_pos, 0, image, group, 2, rotate=True)


def line_barrage(current: tuple, target: tuple, group: pg.sprite.Group, *color: tuple):
    image, target_image = [particle_cache[(3, color[i])] for i in (0, 1)]
    while True:
        if not effective.collidepoint(current):
            break
        Line(color[0], color[1], 0, current, image, target_image, group)
        if math.dist(current, target) < 1e-6:
            break
        current = vector(current, target, 3)[0]


def point_barrage(type: int, color: tuple, locate: tuple, group: pg.sprite.Group):
    image = barrage_cache[(type, color)]
    for _ in range(3):
        pos = (randint(120, 465), randint(15, 225))
        delta = add(locate, inverse(pos))
        angle = direct(*inverse(delta))
        Barrage(effective, 4, color, angle, pos, 0, image, group, 3)


def spawn_particles(group: pg.sprite.Group, size: int, pos: tuple, speeds: tuple, color1: tuple, color2: tuple=None):
    rands = randint(0, 45)
    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else choice([color1, color2])
        speed = uniform(speeds[0], speeds[1])
        image = particle_cache[(size, color)]
        Barrage(effective, speed, color, i, pos, 0, image, group)