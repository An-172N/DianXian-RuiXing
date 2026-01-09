# Copyright (c) 2025, 26 An_172N
# 此代码根据GPLv3.0许可证授权


import random

import SCRIPT.GLOBAL as GLOBAL


def spawn_particles(width, height, pos, speed, color1, color2=None):
    rands = random.randint(0, 45)
    for i in range(0 + rands, 360 + rands, 45):
        color = color1 if color2 == None else random.choice([color1, color2])
        sprite = GLOBAL.char_dict[7]((width, height, 0), color, 1, "particle")
        sprite.speed = random.randint(speed[0], speed[1])
        sprite.rect.center = pos
        sprite.current_angle = i
        GLOBAL.particle_group.add(sprite)