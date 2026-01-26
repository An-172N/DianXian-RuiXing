# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import os

import pygame


class DecisionPoint(pygame.sprite.Sprite):
    asset_path = os.path.join(os.path.dirname(os.path.abspath((__file__))), '..\..\ASSET')
    point_image = pygame.image.load(os.path.join(asset_path, f'IMAGE\IMG_DECISIONPOINT.png')).convert_alpha()

    def __init__(th):
        super().__init__()

        th.original_image = th.point_image
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)