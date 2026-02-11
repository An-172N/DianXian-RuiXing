# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from LOGIC import FUNC, Tool


class Particle(pygame.sprite.Sprite):
    particle_cache = {
        f"{(9, 9)}_{(255, 255, 255)}": Tool.draw_rectangle((9, 9), 0, (255, 255, 255)).convert_alpha(),
        f"{(9, 9)}_{(45, 194, 229)}": Tool.draw_rectangle((9, 9), 0, (45, 194, 229)).convert_alpha(),
        f"{(2, 2)}_{(255, 255, 255)}": Tool.draw_rectangle((2, 2), 0, (255, 255, 255)).convert_alpha(),
        f"{(2, 2)}_{(45, 194, 229)}": Tool.draw_rectangle((2, 2), 0, (45, 194, 229)).convert_alpha(),
        f"{(2, 2)}_{(255, 128, 0)}": Tool.draw_rectangle((2, 2), 0, (255, 128, 0)).convert_alpha(),
        f"{(2, 2)}_{(0, 255, 0)}": Tool.draw_rectangle((2, 2), 0, (0, 255, 0)).convert_alpha(),
        f"{(2, 2)}_{(128, 0, 128)}": Tool.draw_rectangle((2, 2), 0, (128, 0, 128)).convert_alpha(),
        f"{(2, 2)}_{(251, 234, 18)}": Tool.draw_rectangle((2, 2), 0, (251, 234, 18)).convert_alpha(),
        f"{(4, 4)}_{(255, 255, 255)}": Tool.draw_rectangle((4, 4), 0, (255, 255, 255)).convert_alpha(),
        f"{(6, 6)}_{(255, 255, 255)}": Tool.draw_rectangle((6, 6), 0, (255, 255, 255)).convert_alpha(),
        f"{(8, 8)}_{(255, 255, 255)}": Tool.draw_rectangle((8, 8), 0, (255, 255, 255)).convert_alpha(),
        f"{(10, 10)}_{(255, 255, 255)}": Tool.draw_rectangle((10, 10), 0, (255, 255, 255)).convert_alpha(),
        f"{(12, 12)}_{(255, 255, 255)}": Tool.draw_rectangle((12, 12), 0, (255, 255, 255)).convert_alpha(),
    }

    def __init__(th, size: tuple, speed: float, angle: float, pos: tuple, color: tuple, type: str='normal'):
        super().__init__()

        th.speed = speed
        th.current_angle = angle
        th.type = type

        th.is_rotated = False

        th.original_image = Particle.particle_cache[f"{size}_{color}"]
        th.image = th.original_image
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.x, th.y = getattr(th, 'x', th.rect.centerx), getattr(th, 'y', th.rect.centery)
            th.is_rotated = True
        if th.type != 'normal':
            th.speed -= 0.1

            if th.speed < -4:
                th.speed = -4

        rad = math.radians(th.current_angle)
        sin, cos = math.sin(rad), math.cos(rad)
        th.x, th.y = FUNC.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)


def spawn_particles(group: pygame.sprite.Group, size: tuple, pos: tuple, speed: tuple, color1: tuple, color2: tuple=None):
    randint = random.randint
    choice = random.choice
    rands = randint(0, 45)

    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 is None else choice([color1, color2])

        sprite = Particle((size[0], size[1]), randint(speed[0], speed[1]), i, pos, color)

        group.add(sprite)