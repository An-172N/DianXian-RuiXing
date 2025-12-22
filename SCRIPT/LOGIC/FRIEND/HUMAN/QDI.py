import random
import math

import pygame

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.FUNC as FUNC


class Qdi(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 290
        th.color = DICT.color_dict[4]
        th.shape = 2
        th.current_angle = 0

        th.bomb = RandCircle(th.color)

        th.original_image = VARIABLE.char_image["Qdi"]
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
            th.is_free = not th.is_free
            th.choice = random.choice([th.bomb.fire, th.bomb.free])

        th.rect.center = (th.target_x, th.target_y)

        if not th.is_free:
            th.bomb.fire()
        else:
            th.choice()

class RandCircle:
    def __init__(th, color):
        th.color = color

        th.bullet_counter = 0
        th.timer = 0

    def free(th) -> None:
        th.timer += 1

        if th.bullet_counter < 1:
            for _ in range(48):
                x = random.randint(120, 465)
                y = random.randint(15, 250)
                pos = (x, y)
                sprite = DICT.char_dict[7](
                    (9, 9, 0),
                    th.color,
                    2
                )
                sprite.speed = 4
                sprite.rect.center = pos
                sprite.current_angle = random.randint(0, 360)
                VARIABLE.barrage_group.add(sprite)

            th.bullet_counter += 1

    def fire(th) -> None:
        th.timer += 1

        if (
            th.bullet_counter < 6
            and th.timer % 2 == 0
        ):
            char = VARIABLE.main_char
            sprite = DICT.char_dict[7](
                (9, 9, 0),
                th.color,
                2
            )
            sprite.speed = 3.5
            sprite.rect.center = (random.randint(120, 465), random.randint(15, 255))
            x1 = char.rect.centerx
            x2 = sprite.rect.centerx
            y1 = char.rect.centery
            y2 = sprite.rect.centery
            two_pt = FUNC.Calculate.delta_tuple((x1, y1), (x2, y2))
            sprite.current_angle = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
            VARIABLE.barrage_group.add(sprite)

            th.bullet_counter += 1