# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from SCRIPT import SPRITE, char_image
from LOGIC import FUNC


class Qdi(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group, target_pos: tuple):
        super().__init__()

        th.group = group
        th.target_pos = target_pos
        th.particle_group = particle_group

        th.hp = 96
        th.color = (251, 234, 18)

        th.image = char_image.subsurface((60, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.rect.center = (292, 60)
        th.is_free = False
        th.is_die = False
        th.have_power = True
        th.have_flash = False
        th.can_shoot = False
        th.choice = None

        th.target_x, th.target_y = 292, 60
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.particle_counter = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 1:
            for _ in range(48):
                current_angle = random.randint(0, 360)
                sprite_pos = (random.randint(120, 465), random.randint(15, 225))

                sprite = SPRITE.Barrage.Barrage(2, 4, th.color, current_angle, sprite_pos)
                sprite.update()

                th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 6 and th.bullet_timer % 2 == 0:
            sprite_pos = (random.randint(120, 465), random.randint(15, 230))
            two_point = FUNC.add((th.target_pos[0], th.target_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
            current_angle = math.degrees(math.atan2(-two_point[0], -two_point[1]))

            sprite = SPRITE.Barrage.Barrage(2, 3.5, th.color, current_angle, sprite_pos)
            sprite.update()

            th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 150 == 0:
            th.target_x, th.target_y = random.randint(150, 435), random.randint(48, 96)
            th.bullet_counter = 0
            th.particle_counter = 0
            th.can_shoot = True
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free])
        if th.timer % 150 >= 125:
            if th.timer % 150 >= 145:
                th.rect.centerx += random.choice([-4, 4])
            if th.particle_counter <= 0:
                for _ in range(12):
                    pos = (random.randint(th.rect.centerx - 64, th.rect.centerx + 64), random.randint(th.rect.centery - 64, th.rect.centery + 64))
                    two_point = FUNC.add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                    atan2 = math.atan2(-two_point[0], -two_point[1])
                    current_angle = math.degrees(atan2)
                
                    particle = SPRITE.Barrage.Barrage(2, 4, (255, 255, 255), current_angle, pos)

                    th.particle_group.add(particle)

                th.particle_counter += 1
        else:
            th.rect.center = (th.target_x, th.target_y)

        if th.can_shoot:
            th.fire() if not th.is_free else th.choice()

        pygame.sprite.spritecollide(th, th.particle_group, True)