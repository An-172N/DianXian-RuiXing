# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint, choice
from math import degrees, atan2


import pygame


from PRELOAD import color_dict, effective, char_image, barrage_cache
from LOGIC.SPRITE import Barrage, Rect
from LOGIC.TOOL import add, draw_rectangle


class Qdi(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group, target_pos: tuple):
        super().__init__()

        th.group = group
        th.target_pos = target_pos
        th.particle_group = particle_group

        th.hp = 96
        th.color = color_dict[4]

        th.image = char_image.subsurface((60, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.rect.center = (292, 60)
        th.is_free = False
        th.is_die = False
        th.have_power = True
        th.have_flash = False
        th.can_shoot = False

        th.point = None
        th.choice = None

        th.x, th.y = th.rect.center
        th.timer = 0
        th.bullet_counter = 0
        th.bullet_timer = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 1:
            for _ in range(48):
                current_angle = randint(0, 360)
                sprite_pos = (randint(120, 465), randint(15, 225))
                sprite = Barrage.Barrage(effective, 2, 4, th.color, current_angle, sprite_pos, barrage_cache[f"2_{th.color}"], rotate=False)

                th.group.add(sprite)

            th.bullet_counter += 1

    def extend(th) -> None:
        if th.bullet_counter < 1:
            for _ in range(8):
                sprite_pos = (randint(120, 465), randint(15, 205))

                for j in range(0, 360, 30):
                    sprite = Barrage.Barrage(effective, 2, randint(2, 6), th.color, j, sprite_pos, barrage_cache[f"2_{th.color}"], rotate=False)

                    th.group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 6 and th.bullet_timer % 2 == 0:
            sprite_pos = (randint(120, 465), randint(15, 230))
            two_point = add((th.target_pos[0], th.target_pos[1]), (-sprite_pos[0], -sprite_pos[1]))
            current_angle = degrees(atan2(-two_point[0], -two_point[1]))
            sprite = Barrage.Barrage(effective, 2, 3.5, th.color, current_angle, sprite_pos, barrage_cache[f"2_{th.color}"], rotate=False)

            th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 150 == 0:
            th.x, th.y = randint(150, 435), randint(48, 96)
            th.bullet_counter = 0
            th.timer = 0
            th.can_shoot = True
            th.is_free = not th.is_free
            th.choice = choice([th.fire] * 3 + [th.free] * 2 + [th.extend])
        if th.timer % 150 >= 125:
            if th.timer % 150 >= 145:
                th.rect.centerx += choice([-4, 4])
            if th.timer % 125 == 0:
                for _ in range(12):
                    pos = (randint(th.rect.centerx - 64, th.rect.centerx + 64), randint(th.rect.centery - 64, th.rect.centery + 64))
                    two_point = add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    current_angle = degrees(atan2_)
                    particle = Barrage(effective, 2, 4, color_dict[6], current_angle, pos, barrage_cache[f"2_{color_dict[6]}"], False, False)

                    th.particle_group.add(particle)

                th.point = Rect(draw_rectangle((2, 2), 0, color_dict[8]).convert(), th.rect.center, False)
        else:
            th.rect.center = (th.x, th.y)

        if th.point:
            pygame.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.fire() if not th.is_free else th.choice()