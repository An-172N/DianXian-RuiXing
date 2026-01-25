# Copyright (c) 2026 An_172N
# 此代码根据 GPLv3.0 许可证授权


import pygame


class Line(pygame.sprite.Sprite):
    def __init__(th, size: tuple, border: int, damage: int, angle: float, pos: tuple, color: tuple, target_color: tuple):
        super().__init__()

        th.width = size[0]
        th.height = size[1]
        th.border = border
        th.damage = damage
        th.current_angle = angle
        th.color = color
        th.target_color = target_color

        th.type = "line"
        th.timer = 0
        th.is_rotated = False

        th.original_image = th.get_surface()
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos

    def get_surface(th) -> pygame.Surface:
        surface = pygame.Surface((th.width, th.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, th.color, surface.get_rect(), th.border)
            
        return surface
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.mask = pygame.mask.from_surface(th.image)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.is_rotated = True

        th.timer += 1

        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            th.color = th.target_color

            th.image.fill(th.color, special_flags=pygame.BLEND_RGBA_MULT)