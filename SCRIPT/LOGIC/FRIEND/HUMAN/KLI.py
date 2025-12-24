import pygame

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE

class Kli(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.color = DICT.color_dict[5]

        th.bomb = RectRaining(th.color)

        th.original_image = VARIABLE.char_image["Kli"]
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()


class DecisionPoint(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()
        th.original_image = DICT.char_dict[7](
            shape=1,
            type="dec"
        ).image
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)


class RectRaining:
    def __init__(th, color):
        th.color = color

        th.bomb_counter = 0
        th.timer = 0

    def free(th) -> None:
        th.timer += 1

        if (
            th.timer >= 30 and
            th.timer % 1 == 0 and
            th.bomb_counter < 6
        ):
            for i in range(120, 466, 15):
                sprite = DICT.char_dict[7](
                    shape=1,
                    type="bomb"
                )
                if not hasattr(sprite, "damage"):
                    sprite.damage = 6
                sprite.speed = -24
                sprite.rect.center = (i, 0)
                VARIABLE.bullet_group.add(sprite)

            th.bomb_counter += 1

    def fire(th, dx, dy, angle) -> None:
        left = VARIABLE.main_char.rect.left
        top = VARIABLE.main_char.rect.top
        right = VARIABLE.main_char.rect.right
        bullet_type = [
            {
                'x': left - dx,
                'y': top + dy,
                'angle': angle
            },
            {
                'x': right + dx,
                'y': top + dy,
                'angle': -angle
            }
        ]

        for bullet_info in bullet_type:
            sprite = DICT.char_dict[7](
                shape=1,
                type="bullet"
            )
            if not hasattr(sprite, "damage"):
                sprite.damage = 4
            sprite.speed = 16
            sprite.rect.center = (bullet_info['x'], bullet_info['y'])
            sprite.current_angle = bullet_info['angle']
            VARIABLE.bullet_group.add(sprite)