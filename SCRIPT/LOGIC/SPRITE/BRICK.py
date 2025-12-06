import random as rand

import SCRIPT.DICT
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base


def brick_death(brick) -> None:
    if brick.color == SCRIPT.DICT.color_dict[6]:
        process_dict = {
            0: polygon_brick,
            1: line_brick,
            2: circle_brick
        }

        process_dict[brick.shape](
            Base,
            brick,
            VARIABLE.bullet_group,
            16
        )


def circle_brick(sprite, source, sprite_group, speed) -> None:
    rands = rand.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        current_sprite = sprite(
            (2, 15, 0),
            (45, 194, 229),
            1,
            "bullet"
        )
        if not hasattr(current_sprite, "damage"):
            current_sprite.damage = 4
        current_sprite.speed = speed
        current_sprite.rect.center = source.rect.center
        current_sprite.current_angle = i
        current_sprite.update()
        sprite_group.add(current_sprite)


def polygon_brick(sprite, source, sprite_group, speed) -> None:
    midleft = source.rect.midleft
    midright = source.rect.midright
    midbottom = source.rect.midbottom
    bullet_index = [
        {
            'angle': rand.choice([-30, -210]),
            'pos': midleft
        },
        {
            'angle': rand.choice([30, 210]),
            'pos': midright
        },
        {
            'angle': rand.choice([90, 270]),
            'pos': midbottom
        }
    ]

    for bullet_info in bullet_index:
        current_sprite = sprite(
            (2, 15, 0),
            (45, 194, 229),
            1,
            "bullet-cross"
        )
        if not hasattr(current_sprite, "damage"):
            current_sprite.damage = 4
        current_sprite.speed = speed
        current_sprite.rect.center = bullet_info['pos']
        current_sprite.current_angle = bullet_info['angle']
        current_sprite.update()
        sprite_group.add(current_sprite)


def line_brick(sprite, source, sprite_group, _) -> None:
    for _ in range(12):
        current_sprite = sprite(
            (2, rand.randint(30, 180), 0),
            (45, 194, 229),
            1, "bullet"
        )
        if not hasattr(current_sprite, "damage"):
            current_sprite.damage = 6
        current_sprite.speed = 0
        current_sprite.rect.center = source.rect.center
        rands = rand.randint(0, 360)
        current_sprite.current_angle = rands
        current_sprite.update()
        sprite_group.add(current_sprite)