import random
import itertools
import math

import pygame

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE


class Ono(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 192
        th.color = DICT.color_dict[1]
        th.shape = 2
        th.current_angle = 0

        th.original_image = VARIABLE.char_image["Ono"]
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
        th.bullet_counter = 0
        th.bullet_timer = 0
        th.bullet_delay = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if (
            th.bullet_timer % 1 == 0 and
            th.bullet_counter < 12
        ):
            th.bullet_delay += 6

            for i, j in itertools.product(
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 180),
                range(0 + th.bullet_delay, 360 + th.bullet_delay, 90)
            ):
                x = th.rect.centerx + 32 * math.cos(math.radians(i))
                y = th.rect.centery + 32 * math.sin(math.radians(i))
                pos = (x, y)
                sprite = DICT.char_dict[7](
                    color=th.color,
                    shape=2,
                    type="barrage"
                )
                sprite.speed = 3.5
                sprite.rect.center = pos
                sprite.current_angle = j
                VARIABLE.barrage_group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        if th.bullet_counter < 1:
            pos = th.rect.center
            for i in range(0, 360, 15):
                sprite = DICT.char_dict[7](
                    color=th.color,
                    shape=2,
                    type="barrage"
                )
                sprite.speed = 4
                sprite.rect.center = pos
                sprite.current_angle = i
                VARIABLE.barrage_group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            th.target_x = random.choice([150, 220, 292, 365, 435])

            th.bullet_counter = 0
            th.bullet_delay = 0
            th.is_free = not th.is_free
            th.choice = random.choice([th.fire, th.free])

        DICT.char_dict[7].vector(th, 4)

        if not th.is_free:
            th.fire()
        else:
            th.choice()