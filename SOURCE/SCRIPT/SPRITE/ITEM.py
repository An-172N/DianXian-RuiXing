# (C)opyright 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


from PRELOAD import item_cache, particle_cache


class Item(pygame.sprite.Sprite):
    def __init__(th, type: str, speed: float, pos: tuple, size: tuple=(0, 0), color: tuple=(0, 0, 0)):
        super().__init__()

        th.type = type
        th.speed = speed

        if type != "char":
            th.image = item_cache[th.type]
        else:
            th.image = particle_cache[f"{size}_{color}"]
        th.rect = th.image.get_rect(center=pos)

        th.rect.center = pos
        th.x = th.rect.centerx
        th.y = th.rect.centery
    
    def update(th) -> None:
        th.y -= th.speed

        if th.type in ["power", "flash"]:
            th.speed -= 0.1

            if th.speed < -2:
                th.speed = -2
        elif th.type == "char":
            th.speed -= 0.1
            if th.speed < -4:
                th.speed = -4

        th.rect.center = (th.x, th.y)

        if th.rect.centery >= 360:
            th.kill()