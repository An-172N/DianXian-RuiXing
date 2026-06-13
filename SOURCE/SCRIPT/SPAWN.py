# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, sample, uniform


from pygame.sprite import Group


from PRELOAD import *
from LOGIC.CALCULATE import *
from SCRIPT.SPRITE import *


def line_brick(group: Group, pos: tuple):
    rands = (48, 96, 160)
    color1, color2 = color_dict[5], color_dict[9]
    basic_list = [(approximate(randint(0, 360)), choice(rands)) for _ in range(12)]
    filtered_dict = {}
    for a, b in basic_list:
        if a not in filtered_dict or b > filtered_dict[a][1]:
            filtered_dict[a] = (a, b)
    for angle, length in filtered_dict.values():
        image, target_image = [line_cache[(length, angle, i)] for i in (color1, color2)]
        LineBullet(6, pos, image, target_image, group)


def circle_brick(group: Group, pos: tuple):
    image = bullet_cache["bullet"]
    delay = randint(0, 12)
    for i in range(0 + delay, 360 + delay, 12):
        Bullet(effective, 15, 0, i, pos, 4, image, group, form="bullet", rotate=True).update()


def polygon_brick(group: Group, pos1: tuple, pos2: tuple, pos3: tuple):
    image = bullet_cache["bullet"]
    pos = (pos1, pos2, pos3)
    for i, angle in enumerate(range(-30, 91, 60)):
        for j in (0, 1):
            if angle in (30, -30) and j:
                Bullet(effective, 15, 0, angle, pos[i], 4, image, group, form="bullet-cross", rotate=True)
            elif angle == 90:
                angle = angle + j * 180
                Bullet(effective, 15, 0, angle, pos[i], 4, image, group, form="bullet-cross", rotate=True)


def point_brick(group: Group):
    image = bullet_cache["bullet"]
    for _ in range(24):
        pos = (randint(120, 465), randint(15, 320))
        angle = randint(0, 360)
        Bullet(effective, 15, 0, angle, pos, 4, image, group, form="bullet", rotate=True)


def load_brick(row: int, line: str, color: tuple, hp: int, rate: float, size: tuple, interval: tuple):
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            c = color if uniform(0, 1) >= rate else color_dict[6]
            pos = (size[0] + i * interval[0], size[1] + row * interval[1])
            image = brick_cache[(shape, c)]
            brick_ready.append(Brick(shape, hp, c, pos, image))


def choose_brick(group: list, numbers: tuple, power: int, flash: int):
    choose_power = sample(range(len(group)), power + numbers[0] + numbers[1])
    choose_flash = sample(range(len(group)), flash)
    for i in choose_power:
        group[i].power = True
    for i in choose_flash:
        group[i].flash = True


def circle_barrage(type: int, pos: tuple, locate: tuple, group: Group):
    delta = (locate[0] - pos[0], locate[1] - pos[1])
    angle = direct(-delta[0], -delta[1])
    image = barrage_cache[(type, color_dict[6])]
    Barrage(effective, 3, angle, pos, image, group, 3)


def polygon_barrage(type: int, pos: tuple, locate: tuple, group: Group):
    image = barrage_cache[(type, color_dict[6])]
    for i in range(locate[0] - 32, locate[0] + 33, 64):
        delta = (i - pos[0], locate[1] - pos[1])
        angle = direct(-delta[0], -delta[1])
        Barrage(effective, 3, angle, pos, image, group, 2, rotate=True)


def line_barrage(current: tuple, target: tuple, group: Group, color1: tuple, color2: tuple):
    image= particle_cache[(3, color1)]
    start = current
    count = 0
    while True:
        if not effective.collidepoint(current):
            break
        if 327 < current[1] < 336 or current == start:
            Line(color1, color2, 0, current, target, count, image, group)
        if math.dist(current, target) < 1e-6:
            break
        current = vector(current, target, 3)[0]
        count += 1


def point_barrage(type: int, locate: tuple, group: Group):
    image = barrage_cache[(type, color_dict[6])]
    for _ in range(3):
        pos = (randint(120, 465), randint(15, 225))
        delta = (locate[0] - pos[0], locate[1] - pos[1])
        angle = direct(-delta[0], -delta[1])
        Barrage(effective, 4, angle, pos, image, group, 3)


def spawn_particles(group: Group, size: int, pos: tuple, speeds: tuple, color1: tuple, color2: tuple=None):
    rands = randint(0, 60)
    for i in range(0 + rands, 360 + rands, 60):
        color = color1 if color2 is None else choice([color1, color2])
        speed = uniform(speeds[0], speeds[1])
        image = particle_cache[(size, color)]
        Barrage(effective, speed, i, pos, image, group)