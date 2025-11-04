    



    spr.y = getattr(spr, 'y', spr.rect.y)
    spr.vel_y = getattr(spr, 'vel_y', vel_y)

    spr.vel_y += grav

    if spr.vel_y > max_vel:
        spr.vel_y = max_vel

    spr.y += spr.vel_y

    spr.rect.y = int(spr.y)