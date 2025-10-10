import pygame as pyg
import math


def ang(tgt, src):
    dx = tgt.rect.centerx - src.rect.centerx
    dy = tgt.rect.centery - src.rect.centery

    src.curr_ang = math.degrees(math.atan2(-dx, -dy))

    return src.curr_ang


def dist(tgt, src):
    dx = tgt.rect.centerx - src.rect.centerx
    dy = tgt.rect.centery - src.rect.centery

    return math.hypot(dx, dy)


def fric(spr, fric, vel_x=0):
    spr.x = getattr(spr, 'x', spr.rect.x)
    spr.vel_x = getattr(spr, 'vel_x', vel_x)

    spr.vel_x *= fric

    spr.x -= spr.vel_x

    spr.rect.x = int(spr.x)


def grav(spr, grav, vel_y=0, max_vel=2):
    spr.y = getattr(spr, 'y', spr.rect.y)
    spr.vel_y = getattr(spr, 'vel_y', vel_y)

    spr.vel_y += grav

    if spr.vel_y > max_vel:
        spr.vel_y = max_vel

    spr.y += spr.vel_y

    spr.rect.y = int(spr.y)


def mv(spr, spd):
    spr.x = getattr(spr, 'x', spr.rect.x)
    spr.y = getattr(spr, 'y', spr.rect.y)

    spr_rad = math.radians(spr.curr_ang)
    spr.x -= math.sin(spr_rad) * spd
    spr.y -= math.cos(spr_rad) * spd

    spr.rect.x = int(spr.x)
    spr.rect.y = int(spr.y)


def rot(spr):
    if not hasattr(spr, 'orig_image'):
        spr.orig_image = spr.image.copy()

    spr.image = pyg.transform.rotate(spr.orig_image, spr.curr_ang)
    spr.rect = spr.image.get_rect(center=spr.rect.center)


def vec(spr, tar_x, tar_y, spd):
    if not hasattr(spr, 'pos'):
        spr.pos = pyg.math.Vector2(spr.rect.center)

    tar = pyg.math.Vector2(tar_x, tar_y)
    dir = tar - spr.pos
    dis = dir.length()
    
    if dis < spd:
        spr.pos = tar
    else:
        dir = dir.normalize()
        spr.pos += dir * spd

    spr.rect.center = (int(spr.pos.x), int(spr.pos.y))