import random

import SCRIPT.DICT as DICT
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base


def brick_death(brick) -> None:
    if brick.color == DICT.color_dict[6]:
        process_dict = {
            1: circle_brick,
            2: polygon_brick,
            3: line_brick,
            4: point_brick
        }

        process_dict[VARIABLE.stage](
            Base,
            brick,
            VARIABLE.bullet_group,
            16
        )


def circle_brick(sprite, source, sprite_group, speed) -> None:
    rands = random.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        current_sprite = sprite(
            (2, 15, 0),
            DICT.color_dict[5],
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
            'angle': random.choice([-30, -210]),
            'pos': midleft
        },
        {
            'angle': random.choice([30, 210]),
            'pos': midright
        },
        {
            'angle': random.choice([90, 270]),
            'pos': midbottom
        }
    ]

    for bullet_info in bullet_index:
        current_sprite = sprite(
            (2, 15, 0),
            DICT.color_dict[5],
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
            (2, random.randint(30, 180), 0),
            DICT.color_dict[5],
            1, "bullet"
        )
        if not hasattr(current_sprite, "damage"):
            current_sprite.damage = 6
        current_sprite.speed = 0
        current_sprite.rect.center = source.rect.center
        rands = random.randint(0, 360)
        current_sprite.current_angle = rands
        current_sprite.update()
        sprite_group.add(current_sprite)


def point_brick(sprite, _, sprite_group, speed):
    for _ in range(24):
        current_sprite = sprite(
            (2, 15, 0),
            DICT.color_dict[5],
            1, "bullet"
        )
        if not hasattr(current_sprite, "damage"):
            current_sprite.damage = 4
        current_sprite.rect.center = (random.randint(120, 465), random.randint(15, 345))
        rands = random.randint(0, 360)
        current_sprite.current_angle = rands
        current_sprite.speed = speed
        current_sprite.update()
        sprite_group.add(current_sprite)