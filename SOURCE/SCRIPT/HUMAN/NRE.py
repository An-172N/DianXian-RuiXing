# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import randint, choice
from math import degrees, atan2


import pygame


from PRELOAD import color_dict, char_image, effective, particle_cache
from LOGIC.SPRITE import Rect, Barrage
from SCRIPT.SPRITE import Line
from LOGIC.TOOL import vector, add, round_angle, draw_rectangle


class Nre(pygame.sprite.Sprite):
    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group, target_pos: tuple):
        super().__init__()

        th.group = group
        th.target_pos = target_pos
        th.particle_group = particle_group
        th.interval_target_pos = th.target_pos

        th.hp = 256
        th.color = color_dict[3]

        th.image = char_image.subsurface((48, 0, 12, 26))
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
        th.bullet_timer = 0
        th.bullet_counter = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 12:
            start_pos = (randint(120, 465), 15)
            end_pos = (-randint(120, 465), -360)
            delta_pos = add(end_pos, start_pos)
            sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
            current_angle = degrees(atan2(-delta_pos[0], -delta_pos[1]))
            sprite = Line.Line((3, 500), 0, round_angle(current_angle), sprite_pos, color_dict[6], color_dict[3])

            sprite.update()
            th.group.add(sprite)

            th.bullet_counter += 1

    def extend(th) -> None:
        th.bullet_timer += 1

        if th.bullet_counter < 8 and th.bullet_timer % 3 == 0:
            for j in (1, -1):
                start_pos = (th.interval_target_pos[0] + th.bullet_counter * j * 24, 15)
                end_pos = (-(th.interval_target_pos[0] + th.bullet_counter * j * 24), -360)
                delta_pos = add(end_pos, start_pos)
                sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
                sprite = Line.Line((3, 500), 0, 0, sprite_pos, color_dict[6], color_dict[3])

                sprite.update()
                th.group.add(sprite)

            if th.bullet_counter < 1:
                for k in range(8):
                    start_pos = (120, (th.target_pos[1] - 13) - k * 24)
                    end_pos = (-465, -((th.target_pos[1] - 13) - k * 24))
                    delta_pos = add(end_pos, start_pos)
                    sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
                    current_angle = degrees(atan2(-delta_pos[0], -delta_pos[1]))
                    sprite = Line.Line((3, 500), 0, round_angle(current_angle), sprite_pos, color_dict[6], color_dict[3])

                    sprite.update()
                    th.group.add(sprite)
            th.bullet_counter += 1

    def fire(th) -> None:
        if th.bullet_counter < 1:
            for i in range(th.target_pos[0] - 30, th.target_pos[0] + 31, 20):
                start_pos = (i, 15)
                end_pos = (-i, -360)
                delta_pos = add(end_pos, start_pos)
                sprite_pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
                sprite = Line.Line((3, 500), 0, 0, sprite_pos, color_dict[6], color_dict[3])

                sprite.update()
                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 100 == 0:
            th.x = choice((150, 220, 292, 365, 435))
            th.bullet_counter = 0
            th.bullet_timer = 0
            th.timer = 0
            th.interval_target_pos = th.target_pos
            th.can_shoot = True
            th.is_free = not th.is_free
            th.choice = choice([th.fire] + [th.free] * 2 + [th.extend] * 2)
        if th.timer % 100 >= 82:
            if th.timer % 82 == 0:
                for _ in range(8):
                    pos = (randint(th.rect.centerx - 64, th.rect.centerx + 64), th.rect.centery)
                    two_point = add((th.rect.centerx, th.rect.centery), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    current_angle = degrees(atan2_)
                    sprite = Barrage(effective, None, 4, color_dict[6], current_angle, pos, particle_cache[f"{(9, 9)}_{color_dict[6]}"])

                    th.particle_group.add(sprite)

            th.point = Rect(draw_rectangle((2, 2), 0, color_dict[8]).convert(), th.rect.center, False)
        if th.point:
            pygame.sprite.spritecollide(th.point, th.particle_group, True)

        th.rect.center = vector(th.rect.center, (th.x, th.y), 6)[0]

        if th.can_shoot:
            th.fire() if not th.is_free else th.choice()