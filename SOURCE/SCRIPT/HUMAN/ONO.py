# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import random
import math


import pygame


import PRELOAD
from SCRIPT import SPRITE
from LOGIC import Tool


class Ono(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group, target_pos: None):
        super().__init__()

        th.group = group
        th.particle_group = particle_group
        th.target_pos = target_pos

        th.hp = 192
        th.color = PRELOAD.color_dict[1]

        th.image = PRELOAD.char_image.subsurface((24, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.is_free = False
        th.is_die = False
        th.can_shoot = False
        th.have_power = True
        th.have_flash = False

        th.point = None
        th.choice = None

        th.rect.center = (292, 60)
        th.x, th.y = th.rect.center
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.bullet_delay = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 8:
            th.bullet_delay += 6

            for i in range(0 + th.bullet_delay, 360 + th.bullet_delay, 180):
                for j in range(0 + th.bullet_delay, 360 + th.bullet_delay, 90):
                    pos = (th.rect.centerx + 32 * math.cos(math.radians(i)),th.rect.centery + 32 * math.sin(math.radians(i)))
                    sprite = SPRITE.Barrage.Barrage(PRELOAD.effective, 2, 3.5, th.color, j, pos)

                    sprite.update()
                    th.group.add(sprite)

            th.bullet_counter += 1

    def extend(th) -> None:
        speed = 5

        if th.bullet_counter <= 0:
            for _ in range(8):
                for j in range(-30, 31, 30):
                    th.bullet_delay += 20

                    for k in (j - 180, j, 180 - th.bullet_delay):
                        two_point = Tool.add((th.target_pos[0], th.target_pos[1]), (-th.rect.centerx, -th.rect.centery))
                        atan = math.atan2(-two_point[0], -two_point[1])
                        current_angle = math.degrees(atan) + k
                        sprite = SPRITE.Barrage.Barrage(PRELOAD.effective, 2, speed, th.color, current_angle, th.rect.center)

                        sprite.update()
                        th.group.add(sprite)

                speed -= 0.5
            th.bullet_counter += 1

    def fire(th) -> None:
        if th.bullet_counter < 1:
            for i in range(0, 360, 15):
                sprite = SPRITE.Barrage.Barrage(PRELOAD.effective, 2, 4, th.color, i, th.rect.center)

                sprite.update()
                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            rands = random.randint(0, 360)
            th.x, th.y = 292 + 50 * math.cos(math.radians(rands)), 110 + 50 * math.sin(math.radians(rands))
            th.bullet_counter = 0
            th.bullet_delay = 0
            th.timer = 0
            th.can_shoot = True
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free, th.extend])
        if th.timer % 120 >= 99:
            if th.timer % 99 == 0: 
                for i in range(0, 360, 15):
                    pos = (th.rect.centerx + 64 * math.cos(math.radians(i)), th.rect.centery + 64 * math.sin(math.radians(i)))
                    two_point = Tool.add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                    atan2 = math.atan2(-two_point[0], -two_point[1])
                    current_angle = math.degrees(atan2)
                    sprite = SPRITE.Barrage.Barrage(PRELOAD.effective, 2, 4, PRELOAD.color_dict[6], current_angle, pos, False)

                    th.particle_group.add(sprite)

            th.point = SPRITE.Rect.Rect((2, 2), PRELOAD.color_dict[8], th.rect.center)
        if th.point:
            pygame.sprite.spritecollide(th.point, th.particle_group, True)

        th.rect.center = Tool.vector(th.rect.center, (th.x, th.y), 4)[0]

        if th.can_shoot:
            th.fire() if not th.is_free else th.choice()