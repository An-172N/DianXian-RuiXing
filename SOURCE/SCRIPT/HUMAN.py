# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, uniform
from math import radians, sin, cos, atan2, degrees


import pygame as pg


from PRELOAD import *
from LOGIC.PLANE import *
from LOGIC.CALCULATE import *
from LOGIC.DRAW import *
from LOGIC.SPRITE import *
import SCRIPT.SPRITE as Sprite


class Basic(Base):
    __slots__ = ('group', 'particle_group', 'locate', 'hp', 'color', 'is_die', 'can_shoot', 'point', 'choice', 'timer', 'torrent', 'target_pos')

    def __init__(th, image: pg.Surface, locate: tuple, hp: int, color: tuple, *group: pg.sprite.Group):
        super().__init__(None, image, pos=(292, 60))

        th.group = group[0]
        th.particle_group = group[1]
        th.locate = locate
        th.hp = hp
        th.color = color
        th.is_die = False
        th.can_shoot = False
        th.point = None
        th.choice = None
        th.timer = 0
        th.torrent = 0
        th.target_pos = (292, 60)


class Ono(Basic):
    __slots__ = ('power')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((24, 0, 12, 26)), locate, 192, color_dict[1], *group)

        th.power = True

    def fire(th):
        if th.timer == 0:
            for i in range(0, 360, 15):
                Sprite.Barrage(effective, 2, 4, th.color, i, (th.x, th.y), barrage_cache[(2, th.color)], th.group, True, False)

            sound_cache["fire"].play()

    def free(th):
        if th.torrent < 8:
            for i in range(0 + th.timer * 6, 360 + th.timer * 6, 180):
                for j in range(0 + th.timer * 6, 360 + th.timer * 6, 90):
                    pos = (th.x + 32 * cos(radians(i)),th.y + 32 * sin(radians(i)))

                    Sprite.Barrage(effective, 2, 3.5, th.color, j, pos, barrage_cache[(2, th.color)], th.group, True, False)

            th.torrent += 1

            if th.torrent % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        speed = 5
        delay = 0

        if th.timer == 0:
            for _ in range(8):
                for j in range(-30, 31, 30):
                    delay += 20

                    for k in (j - 180, j, 180 - delay):
                        two_point = add(th.locate, (-th.x, -th.y))
                        atan2_ = atan2(-two_point[0], -two_point[1])
                        angle = degrees(atan2_) + k

                        Sprite.Barrage(effective, 2, speed, th.color, angle, (th.x, th.y), barrage_cache[(2, th.color)], th.group, True, False)

                speed -= 0.5

            sound_cache["fire"].play()

    def final(th):
        if th.torrent < 32:
            two_point = add(th.locate, (-th.x, -th.y))
            atan2_ = atan2(-two_point[0], -two_point[1])
            angle = degrees(atan2_) + 180

            for i in (2, 1, -1):
                Sprite.Barrage(effective, 2, 4, th.color, ((th.timer * 12) * i) + angle, (th.x, th.y), barrage_cache[(2, th.color)], th.group, True, False)

            th.torrent += 1

            if th.torrent % 3 == 0:
                sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 120 == 0:
            rands = randint(0, 360)
            th.target_pos = (292 + 50 * cos(radians(rands)), 110 + 50 * sin(radians(rands)))
            th.torrent = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = choice([th.fire] * 5 + [th.free, th.extend, th.final])
        if th.timer % 120 >= 99:
            if th.timer % 99 == 0: 
                for i in range(0, 360, 30):
                    pos = (th.x + 48 * cos(radians(i)), th.y + 48 * sin(radians(i)))
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Sprite.Barrage(effective, 2, 3, color_dict[6], angle, pos, barrage_cache[(2, color_dict[6])], th.particle_group, False, False)

                sound_cache["charge"].play()

                th.point = Sprite.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 4)[0]


class Hro(Basic):
    __slots__ = ('is_choose', 'flash')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((36, 0, 12, 26)), locate, 224, color_dict[2], *group)

        th.is_choose = False
        th.flash = True

    def fire(th):
        if th.timer % 6 == 0 and th.torrent < 3:
            pos = (th.x, th.y)

            for i in range(-30, 31, 30):
                two_point = add((th.locate[0], th.locate[1]), (-pos[0], -pos[1]))
                atan2_ = atan2(-two_point[0], -two_point[1])
                angle = degrees(atan2_) + i

                Sprite.Barrage(effective, 0, 4, th.color, angle, pos, barrage_cache[(0, th.color)], th.group)

            th.torrent += 1
            sound_cache["fire"].play()

    def free(th):
        bullet_type = [
            {
                'dx1': 140,
                'dy1': 140,
                'dx2': 140,
                'dy2': 140
            },
            {
                'dx1': -140,
                'dy1': -140,
                'dx2': 140,
                'dy2': 140
            }
        ]

        if th.torrent < 18:
            for bullet_info in bullet_type:
                start_pos = (292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = (292 - bullet_info['dy1'], 100 + bullet_info['dy2'])
                current_pos, delta_vec = vector(start_pos, end_pos, th.torrent * 25)

                for j in range(45, 136, 90):
                    atan = atan2(-delta_vec.x, -delta_vec.y)
                    angle = degrees(atan) + j + (th.timer * -6)
                    pos = (current_pos.x, current_pos.y)

                    Sprite.Barrage(effective, 0, 4, th.color, angle, pos, barrage_cache[(0, th.color)], th.group)

            th.torrent += 1

            if th.torrent % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        speed = 6

        if th.timer == 0:
            for _ in range(6):
                for j in (150, 185, 220, 255, 292, 327, 365, 400, 435):
                    for k in range(1, 4):
                        pos = (j, 60)
                        two_point = add((th.locate[0], th.locate[1] - 96), (-pos[0], -pos[1]))
                        atan2_ = atan2(-two_point[0], -two_point[1])
                        angle = degrees(atan2_) * k

                        Sprite.Barrage(effective, 0, speed, th.color, angle, pos, barrage_cache[(0, th.color)], th.group)

                speed -= 0.6

            sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 110 == 0:
            th.target_pos = (choice((150, 220, 292, 365)), choice((60, 120, 180, 240)))
            th.torrent = 0
            th.timer = 0
            th.is_choose = False
            th.can_shoot = True
        if th.timer % 110 >= 91:
            if not th.is_choose:
                th.choice = choice([th.fire] * 3 + [th.free, th.extend])
                th.is_choose = True
            if th.timer % 91 == 0:
                for i in range(0, 360, 120 if th.choice == th.fire else 90):
                    pos = (th.x + 45 * cos(radians(i)), th.y + 45 * sin(radians(i)))
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Sprite.Barrage(effective, 0, 3, color_dict[6], angle, pos, barrage_cache[(0, color_dict[6])], th.particle_group, mask=False)

                sound_cache["charge"].play()

                th.point = Sprite.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot and not th.is_choose:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 5)[0]


class Nre(Basic):
    __slots__ = ('power')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((48, 0, 12, 26)), locate, 256, color_dict[3], *group)

        th.power = True

    def fire(th):
        if th.timer == 0:
            for i in range(th.locate[0] - 30, th.locate[0] + 31, 20):
                start_pos = (i, 15)
                end_pos = (-i, -360)
                delta_pos = add(end_pos, start_pos)
                pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)

                Sprite.Line((3, 500), 0, 0, pos, color_dict[6], color_dict[3], th.group, True)

            sound_cache["fire"].play()

    def free(th):
        if th.torrent < 12:
            start_pos = (randint(120, 465), 15)
            end_pos = (-randint(120, 465), -360)
            delta_pos = add(end_pos, start_pos)
            pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
            angle = round_angle(degrees(atan2(-delta_pos[0], -delta_pos[1])))

            Sprite.Line((3, 500), 0, angle, pos, color_dict[6], color_dict[3], th.group, True)

            th.torrent += 1

            if th.torrent % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        if th.torrent < 8 and th.timer % 3 == 0:
            for j in (1, -1):
                start_pos = (th.interval_locate[0] + th.torrent * j * 24, 15)
                end_pos = (-(th.interval_locate[0] + th.torrent * j * 24), -360)
                delta_pos = add(end_pos, start_pos)
                pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)

                Sprite.Line((3, 500), 0, 0, pos, color_dict[6], color_dict[3], th.group, True)

            if th.torrent < 1:
                for k in range(8):
                    start_pos = (120, (th.locate[1] - 13) - k * 24)
                    end_pos = (-465, -((th.locate[1] - 13) - k * 24))
                    delta_pos = add(end_pos, start_pos)
                    pos = (start_pos[0] - delta_pos[0] / 2, start_pos[1] - delta_pos[1] / 2)
                    angle = round_angle(degrees(atan2(-delta_pos[0], -delta_pos[1])))

                    Sprite.Line((3, 500), 0, angle, pos, color_dict[6], color_dict[3], th.group, True)

            th.torrent += 1

            if th.torrent % 2 == 0:
                sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 100 == 0:
            th.target_pos = (choice((150, 220, 292, 365, 435)), 60)
            th.torrent = 0
            th.timer = 0
            th.interval_locate = th.locate
            th.can_shoot = True
            th.choice = choice([th.fire] * 5 + [th.free] * 3 + [th.extend] * 2)
        if th.timer % 100 >= 82:
            if th.timer % 82 == 0:
                for _ in range(8):
                    pos = (int(uniform(th.x - 48, th.x + 48)), th.y)
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Sprite.Barrage(effective, None, 3, color_dict[6], angle, pos, particle_cache[((9, 9), color_dict[6])], th.particle_group, False)

                sound_cache["charge"].play()

                th.point = Sprite.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 6)[0]


class Qdi(Basic):
    __slots__ = ('power')

    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((60, 0, 12, 26)), locate, 96, color_dict[4], *group)

        th.power = True

    def fire(th):
        if th.torrent < 6 and th.timer % 2 == 0:
            pos = (randint(120, 465), randint(15, 230))
            two_point = add(th.locate, (-pos[0], -pos[1]))
            angle = degrees(atan2(-two_point[0], -two_point[1]))

            Sprite.Barrage(effective, 2, 3.5, th.color, angle, pos, barrage_cache[(2, th.color)], th.group, True, False)

            th.torrent += 1

            if th.torrent % 3 == 0:
                sound_cache["fire"].play()

    def free(th):
        if th.timer == 0:
            for _ in range(48):
                angle = randint(0, 360)
                pos = (randint(120, 465), randint(15, 225))

                Sprite.Barrage(effective, 2, 4, th.color, angle, pos, barrage_cache[(2, th.color)], th.group, True, False)

            sound_cache["fire"].play()

    def extend(th):
        if th.timer == 0:
            for _ in range(8):
                pos = (randint(120, 465), randint(15, 200))

                for j in range(0, 360, 30):
                    Sprite.Barrage(effective, 2, randint(2, 5), th.color, j, pos, barrage_cache[(2, th.color)], th.group, True, False)

            sound_cache["fire"].play()

    def final(th):
        if th.timer == 0:
            pos = (randint(120, 465), randint(15, 170))

            for _ in range(10):
                rands = randint(0, 30)

                for i in range(0 + rands, 360 + rands, 30):
                    Sprite.Barrage(effective, 2, randint(2, 5), th.color, i, pos, barrage_cache[(2, th.color)], th.group, True, False)

            sound_cache["fire"].play()

    def last(th):
        if th.timer == 0:
            pos = (randint(150, 435), randint(30, 90))
            target_angle = randint(60, 301)

            for _ in range(10):
                rands = randint(0, 30)

                for i in range(0 + rands, 360 + rands, 30):
                    Sprite.Barrage(effective, 2, uniform(3.5, 4.5) if i <= target_angle + rands else uniform(1.5, 2.5), th.color, i, pos, barrage_cache[(2, th.color)], th.group, True, False)

            sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 150 == 0:
            th.x, th.y = (randint(150, 435), randint(48, 96))
            th.torrent = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = choice([th.fire] * 10 + [th.free] * 2 + [th.extend, th.final, th.last])
        if th.timer % 150 >= 125:
            if th.timer % 150 >= 145:
                th.x += choice([-4, 4])
            if th.timer % 125 == 0:
                for _ in range(12):
                    pos = (int(uniform(th.x - 48, th.x + 48)), int(uniform(th.y - 64, th.y + 64)))
                    two_point = add((th.x, th.y), (-pos[0], -pos[1]))
                    atan2_ = atan2(-two_point[0], -two_point[1])
                    angle = degrees(atan2_)

                    Sprite.Barrage(effective, 2, 3, color_dict[6], angle, pos, barrage_cache[(2, color_dict[6])], th.particle_group, False, False)

                sound_cache["charge"].play()

                th.point = Sprite.Rect(rectangle((2, 2), 0, color_dict[8]).convert(), pos=(th.x, th.y), mask=False)
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()


class Kli(Base):
    __slots__ = ('group', 'particle_group', 'color', 'torrent', 'bullet_timer')

    def __init__(th, *group: pg.sprite.Group):
        super().__init__(None, char_image.subsurface((0, 0, 12, 26)), group[2], pos=(292, 332))

        th.group = group[0]
        th.particle_group = group[1]
        th.color = color_dict[5]
        th.torrent = 0
        th.bullet_timer = 0

    def free(th):
        th.bullet_timer += 1

        if th.bullet_timer == 10:
            for i in range(120, 466, 15):
                pos = (i, randint(345, 360))
                rands = choice([3, 6, 9, 12])

                Sprite.Item('char', uniform(1, 2), pos, th.particle_group, size=(rands, rands), color=color_dict[6])

            sound_cache["charge"].play()

        if th.bullet_timer >= 30 and th.torrent < 6:
            for i in range(120, 466, 15):
                Sprite.Bullet(effective, "bomb", -24, th.color, 0, (i, 0), 6, bullet_cache["bomb"], th.group, mask=False)

            th.torrent += 1

            sound_cache["fire"].play(maxtime=32)

    def fire(th, power: int):
        p = 2 ** (power // 32)
        q = 2 ** (power // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                dx = 0 + i * 10
                dy = 0 + i * 12
                bullet_type = [
                    {
                        'x': th.rect.left - dx,
                        'y': th.rect.top + dy,
                        'angle': j
                    },
                    {
                        'x': th.rect.right + dx,
                        'y': th.rect.top + dy,
                        'angle': -j
                    }
                ]

                for bullet_info in bullet_type:
                    Sprite.Bullet(effective, "bullet", 16, th.color, bullet_info['angle'], (bullet_info['x'], bullet_info['y']), 4, bullet_cache["bullet"], th.group, mask=False)

        sound_cache["fire"].play(maxtime=32)

    def reset_bullet(th):
        th.torrent = 0
        th.bullet_timer = 0