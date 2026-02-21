
import math


import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(th, form: str, hp: int, color: tuple, pos: tuple, image: pygame.Surface):
        super().__init__()

        th.type = form
        th.color = color
        th.hp = hp

        th.have_power = False
        th.have_flash = False
        th.is_die = False

        th.image = image
        th.rect = th.image.get_rect()

        th.rect.center = pos

    def add_power(th) -> None:
        th.have_power = True

    def add_flash(th) -> None:
        th.have_flash = True

    def death(th) -> None:
        th.is_die = True


class Barrage(pygame.sprite.Sprite):
    def __init__(th, effective: pygame.Rect, type: str, speed: float, color: tuple, angle: float, pos: tuple, image: pygame.Surface, mask: bool=True, rotate: bool=True):
        super().__init__()

        th.effective = effective
        th.type = type
        th.speed = speed
        th.color = color
        th.current_angle = angle
        th.can_mask = mask
        th.can_rotate = rotate

        th.is_init = False

        th.original_image = image
        th.image = th.original_image
        th.rect = th.image.get_rect(center=pos)

        th.rect.center = pos
        th.x, th.y = th.rect.center

    def update(th) -> None:
        if not th.is_init:
            if th.can_rotate:
                th.image = pygame.transform.rotate(th.original_image, th.current_angle)
            if th.can_mask:
                th.mask = pygame.mask.from_surface(th.image)
            th.is_init = True
        else:
            rad = math.radians(th.current_angle)
            sin, cos = math.sin(rad), math.cos(rad)
            th.x, th.y = th.x - (sin * th.speed), th.y - (cos * th.speed)
            th.rect.center = (th.x, th.y)

        if not th.effective.collidepoint(th.rect.center):
            th.kill()


class Text(pygame.sprite.Sprite):
    def __init__(th, pos: tuple, kill_time: tuple, speed: float, image: pygame.Surface, target_image: pygame.Surface):
        super().__init__()
        th.target_image = target_image
        th.kill_time = kill_time
        th.speed = speed

        th.image = image
        th.rect = th.image.get_rect()

        th.timer = 0

        th.rect.center = pos
        th.y = th.rect.centery

    def update(th):
        th.timer += 1
        th.y -= th.speed

        th.rect.centery = th.y

        if th.timer >= th.kill_time[1]:
            th.kill()
        elif th.timer >= th.kill_time[0] and th.image != th.target_image:
            th.image = th.target_image


class Rect(pygame.sprite.Sprite):
    def __init__(th, image: pygame.Surface, pos: tuple=(0, 0), mask: bool=False):
        super().__init__()

        th.image = image
        th.rect = th.image.get_rect()
        if mask:
            th.mask = pygame.mask.from_surface(th.image)

        th.rect.center = pos