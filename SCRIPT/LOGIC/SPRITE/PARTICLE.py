import random

import SCRIPT.VARIABLE as VARIABLE
import SCRIPT.DICT as DICT


def spawn_particles(width, height, pos, speed, color1, color2=None):
    rands = random.randint(0, 45)
    for i in range(0 + rands, 360 + rands, 45):
        if color2 is None:
            color = color1
        else:
            color = random.choice([color1, color2])
        sprite = DICT.char_dict[7](
            (width, height, 0),
            color,
            1,
            "particle"
        )
        sprite.speed = random.randint(speed[0], speed[1])
        sprite.rect.center = pos
        sprite.current_angle = i
        VARIABLE.particle_group.add(sprite)