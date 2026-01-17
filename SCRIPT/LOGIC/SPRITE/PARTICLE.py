# Copyright (c) 2026 An_172N
# 此代码根据GPLv3.0许可证授权


import random

from SCRIPT import GLOBAL, LOGIC


def spawn_particles(width: int, height: int, pos: tuple, speed: int, color1: tuple, color2: tuple=()):
    rands = random.randint(0, 45)
    
    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 == () else random.choice([color1, color2])
        sprite = LOGIC.Particle((width, height), random.randint(speed[0], speed[1]), i, color)
        sprite.rect.center = pos
        
        GLOBAL.particle_group.add(sprite)