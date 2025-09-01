import math

def dist(tgt, src):
    dx = tgt.rect.centerx - src.rect.centerx
    dy = tgt.rect.centery - src.rect.centery

    return math.hypot(dx, dy)