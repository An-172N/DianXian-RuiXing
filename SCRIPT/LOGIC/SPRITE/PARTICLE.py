import random

import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.DICT as DICT


def spawn_particles(width, height, color, pos, speed):
    rands = random.randint(0, 45)
    for i in range(0 + rands, 360 + rands, 45):
        sprite = DICT.char_dict[7](
            (width, height, 0),
            color,
            1
        )
        sprite.speed = speed
        sprite.rect.center = pos
        sprite.current_angle = i
        VARIABLE.particle_group.add(sprite)