import random
import math

import SCRIPT.FUNC as FUNC
import SCRIPT.GLOBAL as GLOBAL


def circle_barrage(brick) -> None:
    char_pos = GLOBAL.main_char.rect.center
    sprite = GLOBAL.char_dict[7](
        color=brick.color,
        shape=brick.shape,
        type="barrage"
    )
    sprite.speed = 2
    sprite.rect.center = brick.rect.center
    sprite_pos = sprite.rect.center
    two_pt = FUNC.Calculate.delta_tuple((char_pos[0], char_pos[1]), (sprite_pos[0], sprite_pos[1]))
    sprite.current_angle = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
    sprite.update()
    GLOBAL.barrage_group.add(sprite)


def polygon_barrage(brick) -> None:
    char_pos = GLOBAL.main_char.rect.center
    for i in range(char_pos[0] - 32, char_pos[0] + 33, 64):
        sprite = GLOBAL.char_dict[7](
            color=brick.color,
            shape=brick.shape,
            type="barrage"
        )
        sprite.speed = 2.25
        sprite.rect.center = brick.rect.center
        sprite_pos = sprite.rect.center
        two_pt = FUNC.Calculate.delta_tuple((i, char_pos[1]), (sprite_pos[0], sprite_pos[1]))
        sprite.current_angle = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
        sprite.update()
        GLOBAL.barrage_group.add(sprite)


def line_barrage(_) -> None:
    char_pos = GLOBAL.main_char.rect.center
    start_pos = (random.randint(100, 480), 0)
    end_pos = (char_pos[0], char_pos[1])

    dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
    distance = math.hypot(dpos[0], dpos[1])
                
    sprite = GLOBAL.char_dict[7](
        (2, distance, 0),
        GLOBAL.color_dict[6],
        1,
        "line"
    )
    sprite.speed = 0
    sprite.rect.center = (start_pos[0] + dpos[0] / 2, start_pos[1] + dpos[1] / 2)
    sprite.current_angle = math.degrees(math.atan2(-dpos[0], -dpos[1]))
    sprite.update()
    GLOBAL.barrage_group.add(sprite)


def point_barrage(brick) -> None:
    char_pos = GLOBAL.main_char.rect.center
    for _ in range(3):
        sprite = GLOBAL.char_dict[7](
            color=brick.color,
            shape=brick.shape,
            type="barrage"
        )
        sprite.speed = 3
        sprite.rect.center = (random.randint(120, 465), random.randint(15, 250))
        sprite_pos = sprite.rect.center
        two_point = FUNC.Calculate.delta_tuple((char_pos[0], char_pos[1]), (sprite_pos[0], sprite_pos[1]))
        sprite.current_angle = math.degrees(math.atan2(-two_point[0], -two_point[1]))
        sprite.update()
        GLOBAL.barrage_group.add(sprite)


def spawn_barrage(brick) -> None:
    if random.random() <= 0.25 + GLOBAL.fibonacci_list[GLOBAL.stage - 1]:
        barrage_dict = {
            1: circle_barrage,
            2: polygon_barrage,
            3: line_barrage,
            4: point_barrage
        }
        
        barrage_dict[GLOBAL.stage](brick)