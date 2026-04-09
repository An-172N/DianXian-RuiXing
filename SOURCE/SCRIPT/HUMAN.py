# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, uniform
from math import radians, sin, cos


import pygame as pg


from PRELOAD import *
from LOGIC.CALCULATE import *
from LOGIC.GRAPHIC import *
from LOGIC.SPRITE import *
from SCRIPT.SPAWN import *
from SCRIPT.SPRITE import *


class Basic(Base):
    def __init__(th, image: pg.Surface, hp: int, color: tuple, *group: pg.sprite.Group):
        super().__init__(image, group[2], pos=(292, 60))

        th.group = group[0]
        th.particle_group = group[1]
        th.hp = hp
        th.color = color
        th.is_die = False
        th.can_shoot = False
        th.point = None
        th.choice = None
        th.timer = 0
        th.bullets = 0
        th.index = 0
        th.locate = (0, 0)
        th.target_pos = (292, 60)


class Ono(Basic):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((24, 0, 12, 26)), 192, color_dict[1], *group)

        th.power = True
        th.sd = [th.fire] * 3 + [th.free, th.extend, th.final]

    def fire(th):
        if th.timer == 0:
            for i in range(0, 360, 15):
                Barrage(effective, 2, 4, th.color, i, (th.x, th.y), 0, barrage_cache[(2, th.color)], th.group, 3)

            sound_cache["fire"].play()

    def free(th):
        speed = 5
        delay = 0

        if th.timer == 0:
            for _ in range(8):
                for j in range(-30, 31, 30):
                    delay += 20

                    for k in (j - 180, j, 180 - delay):
                        delta = add(th.locate, (-th.x, -th.y))

                        Barrage(effective, 2, speed, th.color, direct(*inverse(delta)) + k, (th.x, th.y), 0, barrage_cache[(2, th.color)], th.group, 3)

                speed -= 0.5

            sound_cache["fire"].play()

    def extend(th):
        if th.bullets < 10:
            for i in range(0 + th.timer * 7, 360 + th.timer * 7, 180):
                for j in range(0 + th.timer * 7, 360 + th.timer * 7, 90):
                    Barrage(effective, 2, 3.5, th.color, j, (th.x + 32 * cos(radians(i)),th.y + 32 * sin(radians(i))), 0, barrage_cache[(2, th.color)], th.group, 3)

            th.bullets += 1

            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def final(th):
        if th.bullets < 24:
            delta = add(th.locate, (-th.x, -th.y))

            for i in (2, 1, -1, -2):
                Barrage(effective, 2, 4, th.color, ((th.timer * 12) * i) + (direct(*inverse(delta)) + 180), (th.x, th.y), 0, barrage_cache[(2, th.color)], th.group, 3)

            th.bullets += 1

            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 120 == 0:
            rands = randint(0, 360)
            th.target_pos = (292 + 50 * cos(radians(rands)), 110 + 50 * sin(radians(rands)))
            th.bullets = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = th.sd[th.index]
            th.index = (th.index + 1) if th.index < len(th.sd) - 1 else 0
        if th.timer % 99 == 0 and th.timer % 120 >= 99: 
            for i in range(0, 360, 30):
                pos = (th.x + 48 * cos(radians(i)), th.y + 48 * sin(radians(i)))
                delta = add((th.x, th.y), inverse(pos))

                Barrage(effective, 2, 3, color_dict[6], direct(*inverse(delta)), pos, 0, barrage_cache[(2, color_dict[6])], th.particle_group)

            sound_cache["charge"].play()

            th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 4)[0]


class Hro(Basic):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((36, 0, 12, 26)), 224, color_dict[2], *group)

        th.is_choose = False
        th.flash = True
        th.group_index = 1
        th.group_choice = None
        th.sd1 = [th.fire] * 2 + [th.free]
        th.sd2 = [th.fire] * 3 + [th.extend]
        th.sd3 = [th.fire] * 4 + [th.free, th.extend]

    def fire(th):
        if th.timer % 6 == 0 and th.bullets < 3:
            pos = (th.x, th.y)

            for i in range(-30, 31, 30):
                delta = add((th.locate[0], th.locate[1]), inverse(pos))

                Barrage(effective, 0, 4, th.color, direct(*inverse(delta)) + i, pos, 0, barrage_cache[(0, th.color)], th.group, 2)

            th.bullets += 1
            sound_cache["fire"].play()

    def free(th):
        bullet_type = (
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
        )

        if th.bullets < 18:
            for bullet_info in bullet_type:
                start_pos = (292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = (292 - bullet_info['dy1'], 100 + bullet_info['dy2'])
                current_pos, delta_vec = vector(start_pos, end_pos, th.bullets * 25)

                for j in range(45, 136, 90):
                    angle = direct(*inverse(delta_vec)) + j + (th.timer * -6)

                    Barrage(effective, 0, 4, th.color, angle, current_pos, 0, barrage_cache[(0, th.color)], th.group, 2)

            th.bullets += 1

            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        speed = 6

        if th.timer == 0:
            for _ in range(6):
                for j in (150, 185, 220, 255, 292, 327, 365, 400, 435):
                    for k in range(0, 4):
                        pos = (j, 60)
                        delta = add((th.locate[0], th.locate[1] - 160), inverse(pos))

                        Barrage(effective, 0, speed, th.color, direct(*inverse(delta)) + k * 90, pos, 0, barrage_cache[(0, th.color)], th.group, 2)

                speed -= 0.6

            sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 110 == 0:
            th.target_pos = (choice((150, 220, 292, 365)), choice((60, 120, 180, 240)))
            th.bullets = 0
            th.timer = 0
            th.is_choose = False
            th.can_shoot = True
        if th.timer % 110 >= 91:
            if not th.is_choose:
                th.group_choice = th.sd1 if th.group_index == 1 else th.sd2 if th.group_index == 2 else th.sd3
                th.choice = (th.group_choice)[th.index]
                th.index += 1
                if th.index == len(th.group_choice):
                    th.group_index = (th.group_index + 1) if th.group_index < 3 else 1
                    th.index = 0
                th.is_choose = True
            if th.timer % 91 == 0:
                for i in range(0, 360, 120 if th.choice == th.fire else 90):
                    pos = (th.x + 45 * cos(radians(i)), th.y + 45 * sin(radians(i)))
                    delta = add((th.x, th.y), inverse(pos))

                    Barrage(effective, 0, 3, color_dict[6], direct(*inverse(delta)), pos, 0, barrage_cache[(0, color_dict[6])], th.particle_group)

                sound_cache["charge"].play()

                th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot and not th.is_choose:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 5)[0]


class Nre(Basic):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((48, 0, 12, 26)), 256, color_dict[3], *group)

        th.power = True
        th.group_index = 1
        th.group_choice = None
        th.sd1 = [th.fire, th.free, th.fire, th.extend, th.fire, th.final, th.fire, th.last]
        th.sd2 = [th.extend, th.final, th.last]

    def fire(th):
        if th.timer == 0:
            for i in range(th.locate[0] - 30, th.locate[0] + 31, 20):
                line_barrage((i, 15), (i, 345), th.group, color_dict[6], color_dict[3])

            sound_cache["fire"].play()

    def free(th):
        if th.bullets < 16:
            line_barrage((randint(120, 465), 15), (randint(120, 465), 345), th.group, color_dict[6], color_dict[3])

            th.bullets += 1

            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        if th.bullets < 8 and th.timer % 3 == 0:
            for j in (1, -1):
                line_barrage((th.interval_locate[0] + th.bullets * j * 22, 15), ((th.interval_locate[0] + th.bullets * j * 22), 345), th.group, color_dict[6], color_dict[3])

            line_barrage((120, (th.locate[1] - 13) - th.bullets * 22), (465, ((th.locate[1] - 13) - th.bullets * 22)), th.group, color_dict[6], color_dict[3])

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def final(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            line_barrage((220 + th.bullets * 24, 15), ((320 + th.bullets * 24), 345), th.group, color_dict[6], color_dict[3])

            if th.bullets < 6:
                for i in (120, 465):
                    line_barrage((i, 15), (292 + th.bullets * choice([30, -30]), 345), th.group, color_dict[6], color_dict[3])

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def last(th):
        if th.bullets < 20 and th.timer % 2 == 0:
            pos = (th.x + 478 * cos(radians(th.bullets * 18)), th.y + 478 * sin(radians(th.bullets * 18)))
            rands = (randint(120, 465), randint(15, 255))

            line_barrage(th.interval_pos, pos, th.group, color_dict[6], color_dict[3])

            for _ in range(3):
                pos = (rands[0] + 478 * cos(radians(th.bullets * 18)), rands[1] + 478 * sin(radians(th.bullets * 18)))

                line_barrage(rands, pos, th.group, color_dict[6], color_dict[3])

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 100 == 0:
            th.target_pos = (choice((150, 220, 292, 365, 435)), 60)
            th.bullets = 0
            th.timer = 0
            th.interval_pos = th.rect.center
            th.interval_locate = th.locate
            th.can_shoot = True
            th.group_choice = th.sd1 if th.group_index == 1 else th.sd2
            th.choice = (th.group_choice)[th.index]
            th.index += 1
            if th.index == len(th.group_choice):
                th.group_index = (th.group_index + 1) if th.group_index < 2 else 1
                th.index = 0
        if th.timer % 100 >= 82:
            if th.timer % 82 == 0:
                for _ in range(8):
                    pos = (int(uniform(th.x - 48, th.x + 48)), th.y)
                    delta = add((th.x, th.y), inverse(pos))

                    Barrage(effective, None, 3, color_dict[6], direct(*inverse(delta)), pos, 0, particle_cache[(9, color_dict[6])], th.particle_group)

                sound_cache["charge"].play()

                th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 6)[0]


class Qdi(Basic):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((60, 0, 12, 26)), 96, color_dict[4], *group)

        th.power = True

    def fire(th):
        if th.bullets < 6 and th.timer % 2 == 0:
            pos = (randint(120, 465), randint(15, 230))
            delta = add(th.locate, inverse(pos))

            Barrage(effective, 2, 3.5, th.color, direct(*inverse(delta)), pos, 0, barrage_cache[(2, th.color)], th.group, 3)

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def free(th):
        if th.timer == 0:
            for _ in range(64):
                Barrage(effective, 2, 4, th.color, randint(0, 360), (randint(120, 465), randint(15, 225)), 0, barrage_cache[(2, th.color)], th.group, 3)

            sound_cache["fire"].play()

    def extend(th):
        if th.timer == 0:
            for _ in range(8):
                pos = (randint(120, 465), randint(15, 200))
                rands = randint(0, 30)

                for j in range(0 + rands, 360 + rands, 30):
                    Barrage(effective, 2, randint(2, 5), th.color, j, pos, 0, barrage_cache[(2, th.color)], th.group, 3)

            sound_cache["fire"].play()

    def final(th):
        if th.timer == 0:
            pos = (randint(120, 465), randint(15, 170))

            for _ in range(10):
                rands = randint(0, 30)

                for i in range(0 + rands, 360 + rands, 30):
                    Barrage(effective, 2, randint(2, 5), th.color, i, pos, 0, barrage_cache[(2, th.color)], th.group, 3)

            sound_cache["fire"].play()

    def last(th):
        if th.timer == 0:
            target_pos = th.interval_locate
            pos = (randint(120, 465), randint(15, 150))
            delta = add(target_pos, inverse(pos))
            angle = direct(*inverse(delta))
            end = randint(0 + int(angle), 360 + int(angle))

            for i in range(0 + int(angle), 360 + int(angle), 360 // th.target_bullets):
                fast_speed = uniform(6.0, 7.0)
                slow_speed = uniform(3.0, 4.0)
                fast_lose = uniform(0.2, 0.55)
                slow_lose = uniform(0.15, 0.3)

                for _ in range(8):
                    fast_speed -= fast_lose
                    slow_speed -= slow_lose

                    Barrage(effective, 2, fast_speed if i <= end else slow_speed, th.color, i, pos, 0, barrage_cache[(2, th.color)], th.group, 3)

            sound_cache["fire"].play()

    def count(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            for i in range(0, 360, 30):
                Barrage(effective, 2, randint(4, 6), th.color, i + 8 * th.bullets, th.rect.center, 0, barrage_cache[(2, th.color)], th.group, 3)

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 150 == 0:
            th.x, th.y = (randint(150, 435), randint(48, 96))
            th.bullets = 0
            th.timer = 0
            th.interval_locate = th.locate
            th.target_bullets = choice([20, 24, 30, 40])
            th.can_shoot = True
            th.choice = choice([th.fire] * 12 + [th.free] * 2 + [th.extend, th.final, th.last, th.count])
        if th.timer % 150 >= 145:
            th.x += choice([-4, 4])
        if th.timer % 125 == 0 and th.timer % 150 >= 125:
            for _ in range(12):
                pos = (int(uniform(th.x - 48, th.x + 48)), int(uniform(th.y - 64, th.y + 64)))
                delta = add((th.x, th.y), inverse(pos))

                Barrage(effective, 2, 3, color_dict[6], direct(*inverse(delta)), pos, 0, barrage_cache[(2, color_dict[6])], th.particle_group)

            sound_cache["charge"].play()

            th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()


class Kli(Base):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((0, 0, 12, 26)), group[2], pos=(292, 332))

        th.group = group[0]
        th.particle_group = group[1]
        th.color = color_dict[5]
        th.collided = Invinc(180, 6)
        th.divided = Invinc(180, 4, th.reset_bullet)
        th.point = Base(particle_cache[(2, color_dict[6])], radius=1)
        th.bomb_bullets = 0
        th.bullet_timer = 0
        th.bullets = 0
        th.power = 0
        th.is_shoot = True
        th.is_move_right = False
        th.is_move_left = False
        th.is_fast = False

    def fire(th):
        p = 2 ** (th.power // 32)
        q = 2 ** (th.power // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                dx = 0 + i * 10
                dy = 0 + i * 12
                bullet_type = (
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
                )

                for info in bullet_type:
                    Barrage(effective, "bullet", 16, th.color, info['angle'], (info['x'], info['y']), 4, bullet_cache["bullet"], th.group)

        sound_cache["fire"].play(maxtime=32)

    def free(th):
        th.bullet_timer += 1

        if th.bullet_timer == 10:
            for i in range(120, 466, 15):
                pos = (i, randint(345, 360))
                rands = choice([3, 6, 9, 12])

                Barrage(effective, 'char', uniform(1, 2), th.color, 0, pos, 0, particle_cache[(rands, color_dict[6])], th.particle_group)

            sound_cache["charge"].play()

        if th.bullet_timer >= 30 and th.bomb_bullets < 6:
            for i in range(120, 466, 15):
                Barrage(effective, "bomb", -24, th.color, 0, (i, 0), 6, bullet_cache["bomb"], th.group)

            th.bomb_bullets += 1

            sound_cache["fire"].play(maxtime=32)

    def update(th):
        if th.divided.condition:
            th.free()

        th.image = Change.swivel(*[char_image.subsurface((i * 12, 0, 12, 26)) for i in (0, 1)], th.is_move_right, th.is_move_left)
        if th.is_move_left:
            th.x -= 8 if th.is_fast else 3
        if th.is_move_right:
            th.x += 8 if th.is_fast else 3
        th.x = clamp(th.x, window.left, window.right)
        th.y = 331 if th.is_fast else 332
        th.point.rect.center = th.rect.center

        th.divided.update()
        th.collided.update()

        if th.is_shoot and th.bullets > 0:
            th.fire()
            spawn_particles(th.particle_group, 2, th.rect.center, (4, 8), th.color)

            th.bullets -= 1

    def reset_bullet(th):
        th.bomb_bullets = 0
        th.bullet_timer = 0