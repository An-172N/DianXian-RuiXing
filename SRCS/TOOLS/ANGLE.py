import math


def angle(tgt, src):
    dx = tgt.rect.centerx - src.rect.centerx
    dy = tgt.rect.centery - src.rect.centery

    src.curr_ang = math.degrees(math.atan2(-dx, -dy))

    return src.curr_ang