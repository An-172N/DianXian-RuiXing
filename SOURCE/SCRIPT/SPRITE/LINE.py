# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint, choice
from math import degrees, atan2


import pygame


from PRELOAD import line_cache, color_dict
from LOGIC.TOOL import add, round_angle


class Line(pygame.sprite.Sprite):
    def __init__(th, size: tuple, damage: int, angle: float, pos: tuple, color: tuple, target_color: tuple):
        super().__init__()

        th.size = size
        th.damage = damage
        th.current_angle = angle
        th.color = color
        th.target_color = target_color

        th.type = "line"
        th.timer = 0

        th.image = line_cache[(th.size[1], angle, color)]
        th.rect = th.image.get_rect(center=pos)

        th.rect.center = pos

    def update(th) -> None:
        th.timer += 1

        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            th.color = th.target_color
            th.image = line_cache[(th.size[1], th.current_angle, th.color)]


def line_barrage(color: list, target_pos: tuple, group: pygame.sprite.Group) -> None:
    start_pos = (randint(120, 465), 15)
    end_pos = (-target_pos[0], -target_pos[1])
    delta_pos = add(end_pos, start_pos)
    sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
    atan2_ = atan2(-delta_pos[0], -delta_pos[1])
    current_angle = degrees(atan2_)
    sprite = Line((3, 500), 0, round_angle(current_angle), sprite_pos, color[1], color[2])

    sprite.update()
    group.add(sprite)


def line_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    for _ in range(12):
        current_angle = randint(0, 360)
        sprite = Line((2, choice([48, 96, 192])), 6, round_angle(current_angle), spawn_pos, color_dict[5], color_dict[9])

        sprite.update()
        group.add(sprite)