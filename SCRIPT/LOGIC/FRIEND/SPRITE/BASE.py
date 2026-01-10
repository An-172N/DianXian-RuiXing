# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import math

import pygame

import SCRIPT.FUNC as FUNC
import SCRIPT.GLOBAL as GLOBAL


class Base(pygame.sprite.Sprite):
    POLYGON = 0
    RECT = 1
    CIRCLE = 2

    @staticmethod
    def vector(sprite, speed) -> None:
        
        dir = pygame.math.Vector2(sprite.target_x - sprite.rect.centerx, 0)
        current_pos = pygame.math.Vector2(sprite.rect.centerx, sprite.rect.centery)
        target_pos = pygame.math.Vector2(sprite.target_x, 60)

        delta_vec = target_pos - current_pos
        distance = delta_vec.length()

        if distance < speed:
            sprite.rect.center = target_pos
        else:
            if distance > 0:
                dir.normalize_ip()

            new_pos = current_pos + dir * speed
            sprite.rect.center = new_pos

    def __init__(th, value=(0, 0, 0), color=(0, 0, 0), shape=0, type="barrage"):
        super().__init__()
        th.width = value[0]
        th.height = value[1]
        th.border = value[2]
        th.color = color
        th.type = type
        th.shape = shape

        th.current_angle = 0
        th.speed = 0
        th.timer = 0

        th.is_rotated = False
        th.is_visitable = True

        th.original_image = th.get_shape(shape)
        th.image = th.original_image
        th.rect = th.image.get_rect()
        th.mask = pygame.mask.from_surface(th.image)

    def get_shape(th, shape) -> None:
        shape_dict = {
            th.POLYGON: th.polygon,
            th.RECT: th.rectangle,
            th.CIRCLE: th.circle,
        }

        return shape_dict.get(shape)()
    
    def polygon(self) -> pygame.Surface:
        type_dict = {
            "brick": lambda: GLOBAL.sprite_image[f"P_BR_{self.color}"],
            "barrage": lambda: GLOBAL.sprite_image[f"P_BA_{self.color}"]
        }
        
        return type_dict.get(self.type)()

    def rectangle(self) -> pygame.Surface:
        type_dict = {
            "brick": lambda: GLOBAL.sprite_image[f"R_BR_{self.color}"],
            "barrage": lambda:GLOBAL.sprite_image[f"R_BA_{self.color}"],
            "bomb": lambda: GLOBAL.sprite_image[f"KLI_BOMB"],
            "bullet": lambda: GLOBAL.sprite_image[f"KLI_BULLET"],
            "bullet-cross": lambda: GLOBAL.sprite_image[f"KLI_BULLET"],
            "power": lambda: GLOBAL.sprite_image[f"R_IT_{self.color}"],
            "flash": lambda: GLOBAL.sprite_image[f"R_IT_{self.color}"],
            "fire": lambda: GLOBAL.sprite_image[f"R_IT_{self.color}"],
            "dec": lambda: GLOBAL.sprite_image[f"DEC"]
        }

        def not_in_type_dict():
            surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(surface, self.color, surface.get_rect(), self.border)
            return surface
        
        return type_dict.get(self.type, not_in_type_dict)()
            

    def circle(self) -> pygame.Surface:
        type_dict = {
            "brick": lambda: GLOBAL.sprite_image[f"C_BR_{self.color}"],
            "barrage": lambda: GLOBAL.sprite_image[f"C_BA_{self.color}"]
        }

        return type_dict.get(self.type)()
    
    def update(th) -> None:
        if not th.is_rotated:
            th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            th.mask = pygame.mask.from_surface(th.image)
            th.rect = th.image.get_rect(center=th.rect.center)

            th.x = getattr(th, 'x', th.rect.centerx)
            th.y = getattr(th, 'y', th.rect.centery)
            th.is_rotated = True
        
        rad = math.radians(th.current_angle)
        th.x, th.y = FUNC.delta(
            (th.x, th.y),
            (math.sin(rad) * th.speed, math.cos(rad) * th.speed)
        )
        th.rect.center = (th.x, th.y)

        if th.type == "line":
            th.timer += 1

            if th.timer >= 90:
                th.kill()
            elif th.timer >= 45 and th.color != GLOBAL.color_dict[3]:
                th.color = GLOBAL.color_dict[3]

                th.image.fill(th.color, special_flags=pygame.BLEND_RGBA_MULT)