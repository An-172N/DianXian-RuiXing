# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


from random import choice
from math import radians, sin, cos, atan2, degrees


import pygame


from PRELOAD import char_image, effective, color_dict, barrage_cache
from SCRIPT.SPRITE import Barrage
from LOGIC.PLANE import vector
from LOGIC.CALCULATE import add
from LOGIC.DRAW import rectangle
from LOGIC.SPRITE import Base


class Hro(Base):
    __slots__ = ('group', 'particle_group', 'locate', 'hp', 'color', 'is_die', 'is_choose', 'can_shoot', 'have_flash', 'point', 'choice', 'timer', 'bullet_counter', 'target_x', 'target_y')

    def __init__(th, group: pygame.sprite.Group, particle_group: pygame.sprite.Group, locate: tuple):
        super().__init__(None, char_image.subsurface((36, 0, 12, 26)), pos=(292, 60))

        th.group = group
        th.particle_group = particle_group
        th.locate = locate

        th.hp = 224
        th.color = color_dict[2]

        th.is_die = False
        th.is_choose = False
        th.can_shoot = False
        th.have_flash = True

        th.point = None
        th.choice = None

        th.timer = 0
        th.bullet_counter = 0

        th.target_x, th.target_y = (292, 60)

    def death(th) -> None:
        th.is_die = True

    def free(th) -> None:
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

        if th.bullet_counter < 18:
            for bullet_info in bullet_type:
                start_pos = (292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = (292 - bullet_info['dy1'], 100 + bullet_info['dy2'])
                current_pos, delta_vec = vector(start_pos, end_pos, th.bullet_counter * 25)

                for j in range(45, 136, 90):
                    atan = atan2(-delta_vec.x, -delta_vec.y)
                    current_angle = degrees(atan) + j + (th.timer * -6)
                    sprite_pos = (current_pos.x, current_pos.y)
                    sprite = Barrage.Barrage(effective, 0, 4, th.color, current_angle, sprite_pos, barrage_cache[f"0_{th.color}"])

                    sprite.update()
                    th.group.add(sprite)

            th.bullet_counter += 1

    def extend(th) -> None:
        speed = 6

        if th.bullet_counter < 1:
            for _ in range(6):
                for j in (150, 185, 220, 255, 292, 327, 365, 400, 435):
                    for k in range(1, 4):
                        sprite_pos = (j, 60)
                        two_point = add((th.locate[0], th.locate[1] - 96), (-sprite_pos[0], -sprite_pos[1]))
                        atan2_ = atan2(-two_point[0], -two_point[1])
                        current_angle = degrees(atan2_) * k
                        sprite = Barrage.Barrage(effective, 0, speed, th.color, current_angle, sprite_pos, barrage_cache[f"0_{th.color}"])

                        sprite.update()
                        th.group.add(sprite)

                speed -= 0.6
            th.bullet_counter += 1

    def fire(th) -> None:
        if th.timer % 6 == 0 and th.bullet_counter < 3:
            pos = (th.x, th.y)

            for i in range(-30, 31, 30):
                two_point = add((th.locate[0], th.locate[1]), (-pos[0], -pos[1]))
                atan2_ = atan2(-two_point[0], -two_point[1])
                current_angle = degrees(atan2_) + i
                sprite = Barrage.Barrage(effective, 0, 4, th.color, current_angle, pos, barrage_cache[f"0_{th.color}"])

                sprite.update()
                th.group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 110 == 0:
            th.target_x, th.target_y = choice((150, 220, 292, 365)), choice((60, 120, 180, 240))
            th.bullet_counter = 0
            th.timer = 0
            th.is_choose = False
            th.can_shoot = True
        if th.timer % 110 >= 91:
            if not th.is_choose:
                th.choice = choice([th.fire] * 2 + [th.free, th.extend])
                th.is_choose = True
            if th.timer % 91 == 0:
                for i in range(0, 360, 120 if th.choice == th.fire else 90):
                    pos = (th.x + 48 * cos(radians(i)), th.y + 48 * sin(radians(i)))
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    current_angle = degrees(atan2_)
                    particle = Barrage.Barrage(effective, 0, 3, color_dict[6], current_angle, pos, barrage_cache[f"0_{color_dict[6]}"], False)

                    th.particle_group.add(particle)

            th.point = Barrage.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), (th.x, th.y), False)
        if th.point:
            pygame.sprite.spritecollide(th.point, th.particle_group, True)

        th.x, th.y = vector((th.x, th.y), (th.target_x, th.target_y), 5)[0]

        if th.can_shoot and not th.is_choose:
            th.choice()