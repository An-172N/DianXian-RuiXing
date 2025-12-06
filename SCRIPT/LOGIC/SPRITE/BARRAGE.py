import random as rand
import math

import FUNC
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base


def circle_barrage(brick) -> None:
    char = VARIABLE.main_char
    sprite = Base((9, 9, 0), brick.color, brick.shape)
    sprite.speed = 2
    sprite.rect.center = brick.rect.center
    x1 = char.rect.centerx
    x2 = sprite.rect.centerx
    y1 = char.rect.centery
    y2 = sprite.rect.centery
    two_pt = FUNC.Calculate.delta_tuple((x1, y1, 0), (x2, y2, 0))
    sprite.current_angle = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
    VARIABLE.barrage_group.add(sprite)


def polygon_barrage(brick) -> None:
    char = VARIABLE.main_char
    for i in range(char.rect.centerx - 32, char.rect.centerx + 33, 64):
        sprite = Base((9, 9, 0), brick.color, brick.shape)
        sprite.speed = 2.5
        sprite.rect.center = brick.rect.center
        x2 = sprite.rect.centerx
        y1 = char.rect.centery
        y2 = sprite.rect.centery
        two_pt = FUNC.Calculate.delta_tuple((i, y1, 0), (x2, y2, 0))
        sprite.current_angle = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
        VARIABLE.barrage_group.add(sprite)


def line_barrage(_) -> None:
    char = VARIABLE.main_char
    char_x = char.rect.centerx
    char_y = char.rect.centery
    start_pos = (rand.randint(100, 480), 0, 0)
    end_pos = (char_x, char_y, 0)

    dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
    distance = math.hypot(dpos[0], dpos[1])
                
    sprite = Base((2, distance, 0), (255, 255, 255), 1)
    sprite.speed = 0
    x = start_pos[0] + dpos[0] / 2
    y = start_pos[1] + dpos[1] / 2
    sprite.rect.center = (x, y)
    sprite.current_angle = math.degrees(math.atan2(-dpos[0], -dpos[1]))
    sprite.update()
    VARIABLE.barrage_group.add(sprite)


def spawn_barrage(brick) -> None:
    difficulty = FUNC.Calculate.fibonacci(
        0,
        1,
        VARIABLE.stage + 1
    ) / 100
    if rand.random() <= 0.25 + difficulty:
        barrage_dict = {
            0: polygon_barrage,
            1: line_barrage,
            2: circle_barrage
        }
        
        barrage_dict[brick.shape](brick)