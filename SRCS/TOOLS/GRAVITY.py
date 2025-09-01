def grav(spr, grav, max_vel=2):
    spr.y = getattr(spr, 'y', spr.rect.y)

    spr.vel_y += grav

    if spr.vel_y > max_vel:
        spr.vel_y = max_vel

    spr.y += spr.vel_y

    spr.rect.y = int(spr.y)