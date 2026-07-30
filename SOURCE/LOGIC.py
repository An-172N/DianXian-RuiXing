# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议

import math
import os

import pygame


def vector(current, target, step):
    cx, cy = current
    tx, ty = target
    dx, dy = tx - cx, ty - cy
    dist_sq = dx * dx + dy * dy

    if not dist_sq:
        return (tx, ty)

    distance = math.sqrt(dist_sq)
    dx, dy = dx / distance, dy / distance

    if dist_sq < step * step:
        return (tx, ty)
    return (cx + dx * step, cy + dy * step)


def coordinate(position, angle, length):
    radians = math.radians(angle)
    x = position[0] + length * math.cos(radians)
    y = position[1] + length * math.sin(radians)

    return x, y


def clamp(value, minimum, maximum):
    if value > maximum:
        return maximum
    elif value < minimum:
        return minimum
    else:
        return value


def bearing(point_a, point_b):
    ax, ay = point_a
    bx, by = point_b

    return math.degrees(math.atan2(bx - ax, by - ay)) % 360


def record_file(folder, file, content, encode='utf-8'):
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(f'{folder}/{file}', 'w', encoding=encode) as f:
        f.write(content)


def get_files(folder, extension='.dx00', reverse=True):
    files = []
    try:
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            if file.endswith(extension) and os.path.isfile(path):
                time = os.path.getmtime(path)
                files.append((time, path))
        files.sort(key=lambda x: x[0], reverse=reverse)

        return [path for _, path in files]
    except:
        return files


def animate_pop(surface, image_pos_pairs, timer, interval, shortly):
    if shortly:
        surface.fill((0, 0, 0, 0))
        for i in range(len(image_pos_pairs)):
            for j in image_pos_pairs[i]:
                surface.blit(j[0], j[1])
    else:
        for i in range(len(image_pos_pairs)):
            if timer == interval[i]:
                for j in image_pos_pairs[i]:
                    surface.blit(j[0], j[1])


def draw_rectangle(size, border, color):
    return (
        surface := pygame.Surface(size, pygame.SRCALPHA).convert_alpha(),
        pygame.draw.rect(surface, color, surface.get_rect(), border)
    )[0]


def draw_circle(xy_size, border, color):
    return (
        surface := pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA).convert_alpha(),
        pygame.draw.ellipse(surface, color, xy_size, border)
    )[0]


class Base(pygame.sprite.Sprite):
    def __init__(th, original_image, group=None, turn_image=None, form=None, angle=0, pos=(0, 0), radius=None, rotate=False):
        super().__init__(group) if group is not None else super().__init__()
        th.original_image = original_image
        th.turn_image = turn_image
        if turn_image is not None:
            th.turn_image_flipped = pygame.transform.flip(turn_image, True, False)
        th.image = th.original_image if not rotate else pygame.transform.rotate(th.original_image, angle)
        th.rect = th.image.get_rect(center=pos)
        th.angle = angle
        if radius:
            th.radius = radius
        if form is not None:
            th.type = form
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

    def swivel(th, flip, turn):
        if flip:
            th.image = th.turn_image_flipped
        elif turn:
            th.image = th.turn_image
        else:
            th.image = th.original_image


class Invinc:
    def __init__(th, end_time, blink_interval, func=lambda: None, *func_args):
        th.end = end_time
        th.blink_interval = blink_interval
        th.func = func
        th.func_args = func_args
        th.condition = False
        th.visitable = True
        th.timer = 0

    def update(th):
        if th.condition:
            th.timer += 1
            if th.timer >= th.end:
                th.func(*th.func_args)
                th.timer = 0
                th.visitable = True
                th.condition = False
            else:
                th.visitable = (th.timer // th.blink_interval) % 2 == 1


def one_shot(condition, power, critical):
    if not condition and power >= critical:
        condition = True
        power -= critical

    return condition, power


def collide_sprite(sprite1, sprite2):
    if hasattr(sprite1, "start_pos"):
        return sprite2.rect.clipline(*sprite1.start_pos, *sprite1.end_pos)
    elif hasattr(sprite1, 'radius') and hasattr(sprite2, 'radius'):
        return pygame.sprite.collide_circle(sprite1, sprite2)
    else:
        return pygame.sprite.collide_rect(sprite1, sprite2)


def process_lines(content, func, *args):
    return [func(row, line, *args) for row, line in enumerate(content.splitlines())]


def carry(former, latter, start, final):
    if latter >= final:
        former += 1
        latter = start
    else:
        latter += 1

    return former, latter