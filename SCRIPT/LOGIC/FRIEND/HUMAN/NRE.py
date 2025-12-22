import random
import math

import pygame

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.FUNC as FUNC


class Nre(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 256
        th.color = DICT.color_dict[3]
        th.shape = 1
        th.current_angle = 0

        th.bomb = StraightThunder()

        th.original_image = VARIABLE.char_image["Nre"]
        th.image = th.original_image.subsurface(
            (
                0, 0,
                12, 26
            )
        )
        th.rect = th.image.get_rect()

        th.is_free = False
        th.choice = None

        th.target_x = 292
        th.target_y = 60
        th.timer = 0

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            th.target_x = random.choice([150, 220, 292, 365, 435])

            th.bomb.bullet_counter = 0
            th.bomb.timer = 0
            th.is_free = not th.is_free
            th.choice = random.choice([th.bomb.fire, th.bomb.free])

        DICT.char_dict[7].vector(th)

        if not th.is_free:
            th.bomb.fire()
        else:
            th.choice()


class StraightThunder:
    def __init__(th):
        th.timer = 0
        th.bullet_counter = 0

    def free(th) -> None:
        th.timer += 1

        if th.timer % 1 == 0 and th.bullet_counter < 12:
            start_pos = (random.randint(80, 500), 0)
            end_pos = (random.randint(100, 490), 360)

            dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
            distance = math.hypot(dpos[0], dpos[1])

            sprite = DICT.char_dict[7](
                (2, distance, 0),
                DICT.color_dict[6],
                1
            )
            sprite.speed = 0
            sprite.rect.center = (start_pos[0] + dpos[0] / 2, start_pos[1] + dpos[1] / 2)
            sprite.current_angle = math.degrees(math.atan2(-dpos[0], -dpos[1]))
            sprite.update()
            VARIABLE.barrage_group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        if th.bullet_counter < 1:
            char_pos = VARIABLE.main_char.rect.center

            for i in range(char_pos[0] - 30, char_pos[0] + 31, 20):
                end_pos = (i, 360)
                start_pos = (i, 0)

                dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
                distance = math.hypot(dpos[0], dpos[1])

                sprite = DICT.char_dict[7](
                    (2, distance, 0),
                    DICT.color_dict[6],
                    1
                )
                sprite.speed = 0
                sprite.rect.center = (start_pos[0] + dpos[0] / 2, start_pos[1] + dpos[1] / 2)
                sprite.current_angle = 0
                sprite.update()
                VARIABLE.barrage_group.add(sprite)

            th.bullet_counter += 1