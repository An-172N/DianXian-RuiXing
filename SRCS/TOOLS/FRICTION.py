def fric(spr, fric):
    spr.x = getattr(spr, 'x', spr.rect.x)

    spr.vel_x *= fric

    spr.x -= spr.vel_x

    spr.rect.x = int(spr.x)