import math


def mv(spr, spd):
    spr.x = getattr(spr, 'x', spr.rect.x)
    spr.y = getattr(spr, 'y', spr.rect.y)

    spr_rad = math.radians(spr.curr_ang)
    spr.x -= math.sin(spr_rad) * spd
    spr.y -= math.cos(spr_rad) * spd

    spr.rect.x = int(spr.x)
    spr.rect.y = int(spr.y)