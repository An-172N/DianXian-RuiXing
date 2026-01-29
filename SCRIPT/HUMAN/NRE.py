# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math

import pygame

from SCRIPT import SPRITE, char_image
from LOGIC import FUNC, Tool


class Nre(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group, target_pos: tuple):
        super().__init__()

        th.group = group
        th.target_pos = target_pos
        th.particle_group = particle_group

        th.hp = 256
        th.color = (128, 0, 128)

        th.image = char_image.subsurface((48, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False
        th.is_die = False
        th.can_shoot = False
        th.have_power = True
        th.have_flash = False
        th.choice = None

        th.rect.center = (292, 60)
        th.target_x, th.target_y = 292, 60
        th.timer = 0
        th.bullet_timer = 0
        th.bullet_counter = 0
        th.particle_counter = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_timer % 1 == 0 and th.bullet_counter < 12:
            start_pos = (random.randint(80, 500), 0)
            end_pos = (-random.randint(100, 490), -360)

            delta_pos = FUNC.add(end_pos, start_pos)
            distance = math.hypot(delta_pos[0], delta_pos[1])

            sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
            current_angle = math.degrees(math.atan2(-delta_pos[0], -delta_pos[1]))

            sprite = SPRITE.Line.Line((3, distance), 0,current_angle, sprite_pos, (255, 255, 255), (128, 0, 128))
            sprite.update()

            th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        if th.bullet_counter < 1:
            for i in range(th.target_pos[0] - 30, th.target_pos[0] + 31, 20):
                start_pos = (i, 0)
                end_pos = (-i, -360)

                delta_pos = FUNC.add(end_pos, start_pos)
                distance = math.hypot(delta_pos[0], delta_pos[1])
                sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)

                sprite = SPRITE.Line.Line((3, distance), 0, 0, sprite_pos, (255, 255, 255), (128, 0, 128))
                sprite.update()
                
                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 100 == 0:
            th.target_x = random.choice((150, 220, 292, 365, 435))

            th.bullet_counter = 0
            th.bullet_timer = 0
            th.particle_counter = 0
            th.can_shoot = True
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free])
        if th.timer % 100 >= 82 and th.particle_counter <= 0:
            for _ in range(8):
                pos = (random.randint(th.rect.centerx - 64, th.rect.centerx + 64), th.rect.centery)
                two_point = FUNC.add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                atan2 = math.atan2(-two_point[0], -two_point[1])
                current_angle = math.degrees(atan2)

                particle = SPRITE.Particle.Particle((9, 9), 4, current_angle, pos, (255, 255, 255))

                th.particle_group.add(particle)

            th.particle_counter += 1

        th.rect.center = Tool.vector(th.rect.center, (th.target_x, th.target_y), 6)[0]

        if th.can_shoot:
            th.fire() if not th.is_free else th.choice()

        pygame.sprite.spritecollide(th, th.particle_group, True)