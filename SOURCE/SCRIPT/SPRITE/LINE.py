# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint, choice
from math import degrees, atan2


import pygame


from PRELOAD import line_cache, color_dict
from LOGIC.CALCULATE import add, round_angle
from LOGIC.SPRITE import Base


class Line(Base):
    __slots__ = ('size', 'damage', 'color', 'target_color', 'timer')

    def __init__(th, size: tuple, damage: int, angle: float, pos: tuple, color: tuple, target_color: tuple, mask: bool):
        super().__init__("line", line_cache[(size[1], angle, color)], angle, pos=pos, mask=mask)

        th.size = size
        th.damage = damage
        th.color = color
        th.target_color = target_color

        th.timer = 0

    def update(th) -> None:
        th.timer += 1

        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            th.color = th.target_color
            th.image = line_cache[(th.size[1], th.angle, th.color)]


def line_barrage(color: list, locate: tuple, group: pygame.sprite.Group) -> None:
    start_pos = (randint(120, 465), 15)
    end_pos = (-locate[0], -locate[1])
    delta_pos = add(end_pos, start_pos)
    sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
    atan2_ = atan2(-delta_pos[0], -delta_pos[1])
    current_angle = round_angle(degrees(atan2_))
    sprite = Line((3, 500), 0, current_angle, sprite_pos, color[1], color[2], True)

    sprite.update()
    group.add(sprite)


def line_brick(group: pygame.sprite.Group, spawn_pos: tuple) -> None:
    for _ in range(12):
        current_angle = round_angle(randint(0, 360))
        sprite = Line((2, choice([48, 96, 192])), 6, current_angle, spawn_pos, color_dict[5], color_dict[9], False)

        sprite.update()
        group.add(sprite)