# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math
import os

import pygame

from SCRIPT import SPRITE
from LOGIC import FUNC, Tool


class Hro(pygame.sprite.Sprite):
    asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\..\ASSET')
    char_image = pygame.image.load(os.path.join(asset_path, 'IMAGE\IMG_HRO.png')).convert_alpha()

    def __init__(th, group: pygame.sprite.Group, target_pos: tuple):
        super().__init__()

        th.group = group
        th.target_pos = target_pos

        th.hp = 224
        th.color = (0, 255, 0)

        th.image = th.char_image
        th.rect = th.image.get_rect()

        th.is_free = False
        th.is_die = False
        th.have_power = False
        th.have_flash = True
        th.choice = None

        th.rect.center = (292, 60)
        th.target_x = 292
        th.target_y = 60
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.bullet_delay = 0

    def free(th) -> None:
        th.bullet_timer += 1
        th.bullet_delay -= 6

        bullet_type = [
            {
                'dx1': 140,
                'dy1': 140,
                'dx2': 140,
                'dy2': 140
            },
            {
                'dx1': -140,
                'dy1': -140,
                'dx2': 140,
                'dy2': 140
            }
        ]

        if th.bullet_timer % 1 == 0 and th.bullet_counter < 18:
            for bullet_info in bullet_type:
                start_pos = (292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = (292 - bullet_info['dy1'], 100 + bullet_info['dy2'])
                vector = Tool.vector(start_pos, end_pos, th.bullet_counter * 25)
                current_pos = vector[0]
                delta_vec = vector[1]
                
                for j in range(45, 136, 90):
                    atan = math.atan2(-delta_vec.x, -delta_vec.y)
                    current_angle = math.degrees(atan) + j + th.bullet_delay
                    sprite_pos = (current_pos.x, current_pos.y)

                    sprite = SPRITE.Barrage.Barrage(0, 4, th.color, current_angle, sprite_pos)
                    sprite.update()

                    th.group.add(sprite)
        
            th.bullet_counter += 1

    def fire(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer % 6 == 0 and th.bullet_counter < 3:
            pos = th.rect.center

            for i in range(-30, 31, 30):
                two_point = FUNC.add((th.target_pos[0], th.target_pos[1]), (-pos[0], -pos[1]))
                atan = math.atan2(-two_point[0], -two_point[1])
                current_angle = math.degrees(atan) + i

                sprite = SPRITE.Barrage.Barrage(0, 4, th.color, current_angle, pos)
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 110 == 0:
            th.target_x = random.choice((150, 220, 292, 365))
            th.target_y = random.choice((60, 120, 180, 240))

            th.bullet_counter = 0
            th.bullet_delay = 0
            th.is_free = not th.is_free
            th.is_choice = False
            th.choice = random.choice([th.fire, th.free])

        th.rect.center = Tool.vector(th.rect.center, (th.target_x, th.target_y), 5)[0]

        th.fire() if not th.is_free else th.choice()