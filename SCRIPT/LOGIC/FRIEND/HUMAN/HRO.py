import random
import math

import pygame

import SCRIPT.TABLE as TABLE
import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.FUNC as FUNC


class Hro(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 224
        th.color = TABLE.color_dict[2]
        th.shape = 0
        th.current_angle = 0

        th.original_image = VARIABLE.char_image["Hro"]
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

        if (
            th.bullet_timer % 1 == 0
            and th.bullet_counter < 18
        ):
            for bullet_info in bullet_type:
                start_pos = pygame.math.Vector2(292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = pygame.math.Vector2(292 - bullet_info['dy1'], 100 + bullet_info['dy2'])

                delta_pos = end_pos - start_pos
                distance = delta_pos.length()

                if distance > 0:
                    delta_pos.normalize_ip()

                current_step = th.bullet_counter * 24
                current_pos = start_pos + delta_pos * current_step
                
                for j in range(45, 136, 90):
                    sprite = TABLE.char_dict[7](
                        color=th.color,
                        shape=0,
                        type="barrage"
                    )
                    sprite.speed = 4
                    sprite.rect.center = (current_pos.x, current_pos.y)
                    atan = math.atan2(-delta_pos.x, -delta_pos.y)
                    sprite.current_angle = math.degrees(atan) + j + th.bullet_delay
                    TABLE.barrage_group.add(sprite)
        
            th.bullet_counter += 1

    def fire(th) -> None:
        th.bullet_timer += 1

        if (
            th.bullet_timer % 8 == 0
            and th.bullet_counter < 3
        ):
            pos = th.rect.center
            char_pos = VARIABLE.main_char.rect.center
            for i in range(-30, 31, 30):
                sprite = TABLE.char_dict[7](
                    color=th.color,
                    shape=0,
                    type="barrage"
                )
                sprite.speed = 4
                sprite.rect.center = pos
                two_pt = FUNC.Calculate.delta_tuple((char_pos[0], char_pos[1]), (pos[0], pos[1]))
                atan = math.atan2(-two_pt[0], -two_pt[1])
                sprite.current_angle = math.degrees(atan) + i
                TABLE.barrage_group.add(sprite)

            th.bullet_counter += 1

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            th.target_x = random.choice([150, 220, 292, 365, 435])

            th.bullet_counter = 0
            th.bullet_delay = 0
            th.is_free = not th.is_free
            th.is_choice = False
            th.choice = random.choice([th.fire, th.free])

        TABLE.char_dict[7].vector(th, 4.5)

        if not th.is_free:
            th.fire()
        else:
            th.choice()