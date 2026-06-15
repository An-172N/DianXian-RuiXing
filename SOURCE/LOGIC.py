# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


import math
import json
import os


import pygame


def vector(
    current: tuple[float, float],
    target: tuple[float, float],
    step: int,
) -> tuple[tuple[float, float], tuple[float, float]]:
    cx, cy = current
    tx, ty = target
    dx, dy = tx - cx, ty - cy
    dist_sq = dx * dx + dy * dy

    if not dist_sq:
        return (tx, ty), (0.0, 0.0)

    distance = math.sqrt(dist_sq)
    dx, dy = dx / distance, dy / distance

    if dist_sq < step * step:
        return (tx, ty), (dx, dy)
    return (cx + dx * step, cy + dy * step), (dx, dy)


def approximate(
    value: float,
    limit: int = 180,
    step: int = 15
) -> int:
    return 0 if (rounded := round((value % limit) / step) * step) == limit else int(rounded)


def clamp(
    value: float,
    minimum: float,
    maximum: float
) -> float:
    if value > maximum:
        return maximum
    elif value < minimum:
        return minimum
    else:
        return value


def bearing(
    x: float,
    y: float
) -> float:
    return math.degrees(math.atan2(x, y)) % 360


def record_json(
    folder: str,
    file: str,
    content: tuple[str, str],
    encode: str = 'utf-8'
) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)
    dump = [content[0]]
    dump.append(content[1])

    with open(f'{folder}/{file}', 'w', encoding=encode) as f:
        return json.dump(dump, f, indent=4)


def get_files(
    folder: str,
    extension: str = '.json',
    reverse: bool = True
) -> list[str]:
    files = []
    try:
        for file in os.listdir(folder):
            if file.endswith(extension) and os.path.isfile(path := os.path.join(folder, file)):
                time = os.path.getmtime(path)
                files.append((time, path))
        files.sort(key=lambda x: x[0], reverse=reverse)

        return [path for _, path in files]
    except:
        return files
    

def animate_pop(
    surface: pygame.Surface,
    group: tuple[tuple[pygame.Surface, tuple[int, int]], ...],
    timer: int,
    interval: tuple[int, ...],
    shortly: bool,
    color: tuple[int, int, int, int] = (0, 0, 0, 0)
) -> pygame.Surface:
    if shortly:
        surface.fill(color)
        for i in range(len(group)):
            for j in group[i]:
                surface.blit(j[0], j[1])
    else:
        for i in range(len(group)):
            if timer == interval[i]:
                for j in group[i]:
                    surface.blit(j[0], j[1])

    return surface


def draw_rectangle(
    size: tuple[float, float],
    border: int | float,
    color: tuple[int, int, int],
    radius: tuple[int, int, int, int] = (-1, -1, -1, -1)
) -> pygame.Surface:
    return (
        surface := pygame.Surface(size, pygame.SRCALPHA),
        pygame.draw.rect(surface, color, surface.get_rect(), border, -1, *radius)
    )[0]


def draw_circle(
    xy_size: tuple[float, float, float, float],
    border: float,
    color: tuple[int, int, int]
) -> pygame.Surface:
    return (
        surface := pygame.Surface((xy_size[2], xy_size[3]), pygame.SRCALPHA),
        pygame.draw.ellipse(surface, color, xy_size, border)
    )[0]


class Base(pygame.sprite.Sprite):
    def __init__(th,
        original_image: pygame.Surface,
        group: pygame.sprite.Group = None,
        turn_image: pygame.Surface = None,
        form: int | str = None,
        angle: float = 0,
        pos: tuple[int, int] = (0, 0),
        mask: bool = False,
        radius: float = None,
        rotate: bool = False
    ) -> None:
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
        if mask:
            th.mask = pygame.mask.from_surface(th.image)
        if form is not None:
            th.type = form
        th._x, th._y = pos

    @property
    def x(th) -> float:
        return th._x

    @x.setter
    def x(th,
        value: float
    ) -> None:
        th._x = value
        th.rect.centerx = th._x

    @property
    def y(th) -> float:
        return th._y

    @y.setter
    def y(th,
        value: float
    ) -> None:
        th._y = value
        th.rect.centery = th._y

    def swivel(th,
        flip: bool,
        turn: bool
    ) -> None:
        if flip:
            th.image = th.turn_image_flipped
        elif turn:
            th.image = th.turn_image
        else:
            th.image = th.original_image


class Invinc:
    def __init__(th,
        end: int,
        blink_interval: int,
        func: object = lambda: None,
        *func_args: object
    ) -> None:
        th.end = end
        th.blink_interval = blink_interval
        th.func = func
        th.func_args = func_args
        th.condition = False
        th.visitable = True
        th.timer = 0

    def update(th) -> None:
        if th.condition:
            th.timer += 1
            if th.timer >= th.end:
                th.func(*th.func_args)
                th.timer = 0
                th.visitable = True
                th.condition = False
            else:
                th.visitable = (th.timer // th.blink_interval) % 2 == 1


def use_bomb(
    condition: bool,
    power: int,
    critical: int
) -> tuple[bool, int]:
    if not condition and power >= critical:
        condition = True
        power -= critical

    return condition, power


def collide_sprite(
    sprite1: pygame.sprite.Sprite,
    sprite2: pygame.sprite.Sprite
) -> tuple[int, int] | bool | None:
    if hasattr(sprite1, 'mask') and hasattr(sprite2, 'mask'):
        return pygame.sprite.collide_mask(sprite1, sprite2)
    elif hasattr(sprite1, 'radius') and hasattr(sprite2, 'radius'):
        return pygame.sprite.collide_circle(sprite1, sprite2)
    else:
        return pygame.sprite.collide_rect(sprite1, sprite2)


def load_stage(
    file: bytes,
    func: object,
    *args: object,
    decode: str = 'ascii'
) -> list[object]:
    content = []
    arrange = file.decode(decode)
    lines = arrange.splitlines()
    for row, line in enumerate(lines):
        content.append(func(row, line, *args))

    return content


def follow_stage(
    numbers: tuple[int, int],
    end: int,
    start: int = 1
) -> tuple[int, int]:
    stage, level = numbers
    if level >= end:
        stage += 1
        level = start
    else:
        level += 1

    return stage, level