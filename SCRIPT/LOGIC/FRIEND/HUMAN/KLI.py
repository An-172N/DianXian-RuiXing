import pygame

import SCRIPT.GLOBAL as GLOBAL


class Kli(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()

        th.color = GLOBAL.color_dict[5]

        th.original_image = GLOBAL.char_image["Kli"]
        th.image = th.original_image.subsurface((0, 0, 12, 26))
        th.rect = th.image.get_rect()

        th.bullet_counter = 0
        th.bullet_timer = 0

    def free(th) -> None:
        th.bullet_timer += 1

        if (
            th.bullet_timer >= 30 and
            th.bullet_timer % 1 == 0 and
            th.bullet_counter < 6
        ):
            for i in range(120, 466, 15):
                sprite = GLOBAL.char_dict[7](
                    shape=1,
                    type="bomb"
                )
                if not hasattr(sprite, "damage"):
                    sprite.damage = 6
                sprite.speed = -24
                sprite.rect.center = (i, 0)
                GLOBAL.bullet_group.add(sprite)

            th.bullet_counter += 1

    def fire(th, dx, dy, angle) -> None:
        left = GLOBAL.main_char.rect.left
        top = GLOBAL.main_char.rect.top
        right = GLOBAL.main_char.rect.right
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
            sprite = GLOBAL.char_dict[7](
                shape=1,
                type="bullet"
            )
            if not hasattr(sprite, "damage"):
                sprite.damage = 4
            sprite.speed = 16
            sprite.rect.center = (bullet_info['x'], bullet_info['y'])
            sprite.current_angle = bullet_info['angle']
            GLOBAL.bullet_group.add(sprite)


class DecisionPoint(pygame.sprite.Sprite):
    def __init__(th):
        super().__init__()
        th.original_image = GLOBAL.char_dict[7](
            shape=1,
            type="dec"
        ).image
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)