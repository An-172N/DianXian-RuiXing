import random
import math

import pygame

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.FUNC as FUNC


class Hro(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.hp = 224
        th.color = DICT.color_dict[2]
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

        th.bomb = PolyX(th.color, th.rect)

        th.is_free = False
        th.choice = None

        th.target_x = 292
        th.target_y = 60
        th.timer = 0

    def update(th) -> None:
        th.timer += 1

        if th.timer % 120 == 0:
            th.target_x = random.choice([150, 220, 292, 365, 435])

            th.bomb.bullet_cnt = 0
            th.bomb.dl = 0
            th.is_free = not th.is_free
            th.is_choice = False
            th.choice = random.choice([th.bomb.fire, th.bomb.free])

        dir = pygame.math.Vector2(th.target_x - th.rect.centerx, 0)
        current_pos = pygame.math.Vector2(th.rect.centerx, th.rect.centery)
        target_pos = pygame.math.Vector2(th.target_x, 60)

        delta_vec = target_pos - current_pos
        distance = delta_vec.length()

        if distance < 4:
            th.rect.center = target_pos
        else:
            if distance > 0:
                dir.normalize_ip()

            new_pos = current_pos + dir * 4
            th.rect.center = new_pos

        if not th.is_free:
            th.bomb.fire()
        else:
            th.choice()


class PolyX:
    def __init__(th, color, rect):
        th.color = color
        th.rect = rect

        th.bullet_cnt = 0
        th.timer = 0
        th.dl = 0

    def free(th) -> None:
        th.timer += 1
        th.dl -= 6

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

        if th.timer % 1 == 0 and th.bullet_cnt < 18:
            for bullet_info in bullet_type:
                start_pos = pygame.math.Vector2(292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = pygame.math.Vector2(292 - bullet_info['dy1'], 100 + bullet_info['dy2'])

                delta_pos = end_pos - start_pos
                distance = delta_pos.length()

                if distance > 0:
                    delta_pos.normalize_ip()

                current_step = th.bullet_cnt * 24
                current_pos = start_pos + delta_pos * current_step
                
                for j in range(45, 136, 90):
                    sprite = DICT.char_dict[7](
                        (9, 9, 0),
                        th.color,
                        0
                    )
                    sprite.speed = 4
                    sprite.rect.center = (current_pos.x, current_pos.y)
                    atan = math.atan2(-delta_pos.x, -delta_pos.y)
                    sprite.current_angle = math.degrees(atan) + j + th.dl
                    VARIABLE.barrage_group.add(sprite)
        
            th.bullet_cnt += 1

    def fire(th) -> None:
        th.timer += 1

        if th.timer % 8 == 0 and th.bullet_cnt < 3:
            pos = th.rect.center
            char_pos = VARIABLE.main_char.rect.center
            for i in range(-30, 31, 30):
                sprite = DICT.char_dict[7](
                    (9, 9, 0),
                    th.color,
                    0
                )
                sprite.speed = 4
                sprite.rect.center = pos
                two_pt = FUNC.Calculate.delta_tuple((char_pos[0], char_pos[1]), (pos[0], pos[1]))
                atan = math.atan2(-two_pt[0], -two_pt[1])
                sprite.current_angle = math.degrees(atan) + i
                VARIABLE.barrage_group.add(sprite)

            th.bullet_cnt += 1