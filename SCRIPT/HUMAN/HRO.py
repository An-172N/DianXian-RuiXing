# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from SCRIPT import SPRITE, char_image
from LOGIC import FUNC, Tool


class Hro(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group, target_pos: tuple):
        super().__init__()

        th.group = group
        th.particle_group = particle_group
        th.target_pos = target_pos

        th.hp = 224
        th.color = (0, 255, 0)

        th.image = char_image.subsurface((36, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.is_die = False
        th.is_choose = False
        th.can_shoot = False
        th.have_power = False
        th.have_flash = True

        th.point = None
        th.choice = None

        th.rect.center = (292, 60)
        th.target_x, th.target_y = 292, 60
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.bullet_delay = 0
        th.particle_counter = 0

    def free(th) -> None:
        barrage = SPRITE.Barrage.Barrage
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
                current_pos, delta_vec = Tool.vector(start_pos, end_pos, th.bullet_counter * 25)
                
                for j in range(45, 136, 90):
                    atan = math.atan2(-delta_vec.x, -delta_vec.y)
                    current_angle = math.degrees(atan) + j + th.bullet_delay
                    sprite_pos = (current_pos.x, current_pos.y)

                    sprite = barrage(0, 4, th.color, current_angle, sprite_pos)
                    sprite.update()

                    th.group.add(sprite)
        
            th.bullet_counter += 1

    def fire(th) -> None:
        barrage = SPRITE.Barrage.Barrage
        th.bullet_timer += 1

        if th.bullet_timer % 6 == 0 and th.bullet_counter < 3:
            pos = th.rect.center

            for i in range(-30, 31, 30):
                two_point = FUNC.add((th.target_pos[0], th.target_pos[1]), (-pos[0], -pos[1]))
                atan = math.atan2(-two_point[0], -two_point[1])
                current_angle = math.degrees(atan) + i

                sprite = barrage(0, 4, th.color, current_angle, pos)
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        choice = random.choice
        radians = math.radians
        th.timer += 1

        if th.timer % 110 == 0:
            th.target_x, th.target_y = choice((150, 220, 292, 365)), choice((60, 120, 180, 240))
            th.bullet_counter = 0
            th.bullet_delay = 0
            th.particle_counter = 0
            th.is_choose = False
            th.can_shoot = True
        if th.timer % 110 >= 91 and th.particle_counter <= 0:
            if not th.is_choose:
                th.choice = choice([th.fire, th.fire, th.free])
                th.is_choose = True
            for i in range(0, 360, 120 if th.choice == th.fire else 90):
                pos = (th.rect.centerx + 64 * math.cos(radians(i)), th.rect.centery + 64 * math.sin(radians(i)))
                two_point = FUNC.add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                atan2 = math.atan2(-two_point[0], -two_point[1])
                current_angle = math.degrees(atan2)

                particle = SPRITE.Barrage.Barrage(0, 4, (255, 255, 255), current_angle, pos)

                th.particle_group.add(particle)

            th.particle_counter += 1
            th.point = SPRITE.Rect.Rect((2, 2), 0, (0, 0, 0), th.rect.center)
        if th.point:
            pygame.sprite.spritecollide(th.point, th.particle_group, True)

        th.rect.center = Tool.vector(th.rect.center, (th.target_x, th.target_y), 5)[0]

        if th.can_shoot and not th.is_choose:
            th.choice()