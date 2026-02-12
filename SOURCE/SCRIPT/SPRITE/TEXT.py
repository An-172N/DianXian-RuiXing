# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame

import PRELOAD


class Text(pygame.sprite.Sprite):
    def __init__(th, type: str, pos: tuple, target_color: tuple):
        super().__init__()

        th.type = type
        th.target_color = target_color
        th.color = (255, 255, 255)

        try:
            th.image = PRELOAD.text_cache[f"{th.type}_{th.color}"]
        except KeyError:
            th.image = PRELOAD.font.render(th.type, False, (255, 255, 255))
        th.rect = th.image.get_rect()

        th.timer = 0

        th.rect.center = pos
        th.y = th.rect.centery

    def update(th):
        th.timer += 1
        th.y -= 0.5
        th.rect.centery = th.y

        if th.timer >= 60:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            try:
                th.image = PRELOAD.text_cache[f"{th.type}_{th.target_color}"]
            except KeyError:
                th.image = PRELOAD.font.render(th.type, False, th.target_color)