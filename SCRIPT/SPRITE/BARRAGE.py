# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import math
import os

import pygame

from SCRIPT import FUNC


class Barrage(pygame.sprite.Sprite):
    asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\..\ASSET')
    barrage_image = {
        key: pygame.image.load(file).convert_alpha() for key, file in [
            (f"C_BA_{(255, 128, 0)}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEORANGE.png')),
            (f"C_BA_{(251, 234, 18)}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEYELLOW.png')),
            (f"C_BA_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_CIRCLEBARRAGEWHITE.png')),
            (f"T_BA_{(0, 255, 0)}", os.path.join(asset_path, f'IMAGE\IMG_TRIANGLEBARRAGEGREEN.png')),
            (f"T_BA_{(255, 255, 255)}", os.path.join(asset_path, f'IMAGE\IMG_TRIANGLEBARRAGEWHITE.png'))
        ]
    }

    def __init__(th, type: str, speed: float, color: tuple, angle: float, pos: tuple):
        super().__init__()

        th.type = type
        th.speed = speed
        th.color = color
        th.current_angle = angle

        th.is_rotated = False

        th.original_image = th.get_type(type)
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos

    def get_type(th, type: int) -> pygame.Surface:
        bullet_dict = {
            0: lambda: Barrage.barrage_image[f"T_BA_{th.color}"],
            2: lambda: Barrage.barrage_image[f"C_BA_{th.color}"]
        }

        return bullet_dict.get(type)()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.mask = pygame.mask.from_surface(th.image)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.x = getattr(th, 'x', th.rect.centerx)
            th.y = getattr(th, 'y', th.rect.centery)

            th.is_rotated = True

        rad = math.radians(th.current_angle)
        sin = math.sin(rad)
        cos = math.cos(rad)
        th.x, th.y = FUNC.add((th.x, th.y), (-(sin * th.speed), -(cos * th.speed)))
        th.rect.center = (th.x, th.y)