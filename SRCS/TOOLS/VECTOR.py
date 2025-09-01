import pygame as pyg


def vec(spr, vel):
    if not hasattr(spr, 'pos'):
        spr.pos = pyg.math.Vector2(spr.rect.center)
    
    spr.pos += vel
    spr.rect.center = (int(spr.pos.x), int(spr.pos.y))