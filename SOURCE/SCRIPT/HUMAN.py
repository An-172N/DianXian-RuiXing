# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议


from random import choice, randint, uniform
from math import radians, sin, cos


import pygame as pg


from PRELOAD import *
from LOGIC.CALCULATE import *
from LOGIC.GRAPHIC import *
from LOGIC.SPRITE import *
import SCRIPT.SPRITE as Sprite


class Basic(Base):
    def __init__(th, image: pg.Surface, locate: tuple, hp: int, color: tuple, *group: pg.sprite.Group):
        super().__init__(image, group[2], pos=(292, 60))

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
        th.bullets = 0
        th.target_pos = (292, 60)


class Ono(Basic):
    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((24, 0, 12, 26)), locate, 192, color_dict[1], *group)

        th.power = True

    def fire(th):
        if th.timer == 0:
            for i in range(0, 360, 15):
                Sprite.Barrage(effective, 2, 4, th.color, i, (th.x, th.y), barrage_cache[(2, th.color)], th.group, rotate=False)

            sound_cache["fire"].play()

    def free(th):
        if th.bullets < 10:
            for i in range(0 + th.timer * 7, 360 + th.timer * 7, 180):
                for j in range(0 + th.timer * 7, 360 + th.timer * 7, 90):
                    pos = (th.x + 32 * cos(radians(i)),th.y + 32 * sin(radians(i)))

                    Sprite.Barrage(effective, 2, 3.5, th.color, j, pos, barrage_cache[(2, th.color)], th.group, rotate=False)

            th.bullets += 1

            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        speed = 5
        delay = 0

        if th.timer == 0:
            for _ in range(8):
                for j in range(-30, 31, 30):
                    delay += 20

                    for k in (j - 180, j, 180 - delay):
                        delta = add(th.locate, (-th.x, -th.y))
                        angle = direct(-delta[0], -delta[1]) + k

                        Sprite.Barrage(effective, 2, speed, th.color, angle, (th.x, th.y), barrage_cache[(2, th.color)], th.group, rotate=False)

                speed -= 0.5

            sound_cache["fire"].play()

    def final(th):
        if th.bullets < 24:
            delta = add(th.locate, (-th.x, -th.y))
            angle = direct(-delta[0], -delta[1]) + 180

            for i in (2, 1, -1, -2):
                Sprite.Barrage(effective, 2, 4, th.color, ((th.timer * 12) * i) + angle, (th.x, th.y), barrage_cache[(2, th.color)], th.group, rotate=False)

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
            th.choice = choice([th.fire] * 5 + [th.free, th.extend, th.final])
        if th.timer % 99 == 0 and th.timer % 120 >= 99: 
            for i in range(0, 360, 30):
                pos = (th.x + 48 * cos(radians(i)), th.y + 48 * sin(radians(i)))
                delta = add((th.x, th.y), (-pos[0], -pos[1]))
                angle = direct(-delta[0], -delta[1])

                Sprite.Barrage(effective, 2, 3, color_dict[6], angle, pos, barrage_cache[(2, color_dict[6])], th.particle_group, rotate=False)

            sound_cache["charge"].play()

            th.point = Sprite.Rect(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 4)[0]


class Hro(Basic):
    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((36, 0, 12, 26)), locate, 224, color_dict[2], *group)

        th.is_choose = False
        th.flash = True

    def fire(th):
        if th.timer % 6 == 0 and th.bullets < 3:
            pos = (th.x, th.y)

            for i in range(-30, 31, 30):
                delta = add((th.locate[0], th.locate[1]), (-pos[0], -pos[1]))
                angle = direct(-delta[0], -delta[1]) + i

                Sprite.Barrage(effective, 0, 4, th.color, angle, pos, barrage_cache[(0, th.color)], th.group, radius=4)

            th.bullets += 1
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

        if th.bullets < 18:
            for bullet_info in bullet_type:
                start_pos = (292 + bullet_info['dx1'], 100 - bullet_info['dx2'])
                end_pos = (292 - bullet_info['dy1'], 100 + bullet_info['dy2'])
                current_pos, delta_vec = vector(start_pos, end_pos, th.bullets * 25)

                for j in range(45, 136, 90):
                    angle = direct(-delta_vec[0], -delta_vec[1]) + j + (th.timer * -6)
                    pos = current_pos

                    Sprite.Barrage(effective, 0, 4, th.color, angle, pos, barrage_cache[(0, th.color)], th.group, radius=4)

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
                        delta = add((th.locate[0], th.locate[1] - 160), (-pos[0], -pos[1]))
                        angle = direct(-delta[0], -delta[1]) + k * 90

                        Sprite.Barrage(effective, 0, speed, th.color, angle, pos, barrage_cache[(0, th.color)], th.group, radius=4)

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
                th.choice = choice([th.fire] * 3 + [th.free, th.extend])
                th.is_choose = True
            if th.timer % 91 == 0:
                for i in range(0, 360, 120 if th.choice == th.fire else 90):
                    pos = (th.x + 45 * cos(radians(i)), th.y + 45 * sin(radians(i)))
                    delta = add((th.x, th.y), (-pos[0], -pos[1]))
                    angle = direct(-delta[0], -delta[1])

                    Sprite.Barrage(effective, 0, 3, color_dict[6], angle, pos, barrage_cache[(0, color_dict[6])], th.particle_group)

                sound_cache["charge"].play()

                th.point = Sprite.Rect(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot and not th.is_choose:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 5)[0]


class Nre(Basic):
    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((48, 0, 12, 26)), locate, 256, color_dict[3], *group)

        th.power = True

    def fire(th):
        if th.timer == 0:
            for i in range(th.locate[0] - 30, th.locate[0] + 31, 20):
                start_pos = (i, 15)
                end_pos = (i, 345)

                Sprite.line_barrage([None, color_dict[6], color_dict[3]], start_pos, end_pos, th.group)

            sound_cache["fire"].play()

    def free(th):
        if th.bullets < 16:
            start_pos = (randint(120, 465), 15)
            end_pos = (randint(120, 465), 345)

            Sprite.line_barrage([None, color_dict[6], color_dict[3]], start_pos, end_pos, th.group)

            th.bullets += 1

            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        if th.bullets < 8 and th.timer % 3 == 0:
            for j in (1, -1):
                start_pos = (th.interval_locate[0] + th.bullets * j * 22, 15)
                end_pos = ((th.interval_locate[0] + th.bullets * j * 22), 345)

                Sprite.line_barrage([None, color_dict[6], color_dict[3]], start_pos, end_pos, th.group)

            start_pos = (120, (th.locate[1] - 13) - th.bullets * 22)
            end_pos = (465, ((th.locate[1] - 13) - th.bullets * 22))

            Sprite.line_barrage([None, color_dict[6], color_dict[3]], start_pos, end_pos, th.group)

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def final(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            start_pos = (220 + th.bullets * 24, 15)
            end_pos = ((320 + th.bullets * 24), 345)

            Sprite.line_barrage([None, color_dict[6], color_dict[3]], start_pos, end_pos, th.group)

            if th.bullets < 6:
                for i in (120, 465):
                    start_pos = (i, 15)
                    end_pos = (292 + th.bullets * choice([30, -30]), 345)

                    Sprite.line_barrage([None, color_dict[6], color_dict[3]], start_pos, end_pos, th.group)

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def update(th):
        th.timer += 1

        if th.timer % 100 == 0:
            th.target_pos = (choice((150, 220, 292, 365, 435)), 60)
            th.bullets = 0
            th.timer = 0
            th.interval_locate = th.locate
            th.can_shoot = True
            th.choice = choice([th.fire] * 6 + [th.free] * 3 + [th.extend] * 2 + [th.final])
        if th.timer % 100 >= 82:
            if th.timer % 82 == 0:
                for _ in range(8):
                    pos = (int(uniform(th.x - 48, th.x + 48)), th.y)
                    delta = add((th.x, th.y), (-pos[0], -pos[1]))
                    angle = direct(-delta[0], -delta[1])

                    Sprite.Barrage(effective, None, 3, color_dict[6], angle, pos, particle_cache[(9, color_dict[6])], th.particle_group)

                sound_cache["charge"].play()

                th.point = Sprite.Rect(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

        th.x, th.y = vector((th.x, th.y), th.target_pos, 6)[0]


class Qdi(Basic):
    def __init__(th, locate: tuple, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((60, 0, 12, 26)), locate, 96, color_dict[4], *group)

        th.power = True

    def fire(th):
        if th.bullets < 6 and th.timer % 2 == 0:
            pos = (randint(120, 465), randint(15, 230))
            delta = add(th.locate, (-pos[0], -pos[1]))
            angle = direct(-delta[0], -delta[1])

            Sprite.Barrage(effective, 2, 3.5, th.color, angle, pos, barrage_cache[(2, th.color)], th.group, rotate=False)

            th.bullets += 1

            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def free(th):
        if th.timer == 0:
            for _ in range(48):
                angle = randint(0, 360)
                pos = (randint(120, 465), randint(15, 225))

                Sprite.Barrage(effective, 2, 4, th.color, angle, pos, barrage_cache[(2, th.color)], th.group, rotate=False)

            sound_cache["fire"].play()

    def extend(th):
        if th.timer == 0:
            for _ in range(8):
                pos = (randint(120, 465), randint(15, 200))
                rands = randint(0, 30)

                for j in range(0 + rands, 360 + rands, 30):
                    Sprite.Barrage(effective, 2, randint(2, 5), th.color, j, pos, barrage_cache[(2, th.color)], th.group, rotate=False)

            sound_cache["fire"].play()

    def final(th):
        if th.timer == 0:
            pos = (randint(120, 465), randint(15, 170))

            for _ in range(10):
                rands = randint(0, 30)

                for i in range(0 + rands, 360 + rands, 30):
                    Sprite.Barrage(effective, 2, randint(2, 5), th.color, i, pos, barrage_cache[(2, th.color)], th.group, rotate=False)

            sound_cache["fire"].play()

    def last(th):
        if th.timer == 0:
            target_pos = th.interval_locate
            pos = (randint(120, 465), randint(15, 150))
            delta = add(target_pos, (-pos[0], -pos[1]))
            angle = direct(-delta[0], -delta[1])
            end = randint(0 + int(angle), 360 + int(angle))

            for i in range(0 + int(angle), 360 + int(angle), 360 // th.target_bullets):
                fast_speed = uniform(6.0, 7.0)
                slow_speed = uniform(3.0, 4.0)
                fast_lose = uniform(0.2, 0.55)
                slow_lose = uniform(0.15, 0.3)

                for _ in range(8):
                    fast_speed -= fast_lose
                    slow_speed -= slow_lose
                    speed = fast_speed if i <= end else slow_speed

                    Sprite.Barrage(effective, 2, speed, th.color, i, pos, barrage_cache[(2, th.color)], th.group, rotate=False)

            sound_cache["fire"].play()

    def count(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            for i in range(0, 360, 30):
                speed = randint(4, 6)
                pos = th.rect.center
                angle = i + 8 * th.bullets

                Sprite.Barrage(effective, 2, speed, th.color, angle, pos, barrage_cache[(2, th.color)], th.group, rotate=False)

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
                delta = add((th.x, th.y), (-pos[0], -pos[1]))
                angle = direct(-delta[0], -delta[1])

                Sprite.Barrage(effective, 2, 3, color_dict[6], angle, pos, barrage_cache[(2, color_dict[6])], th.particle_group, rotate=False)

            sound_cache["charge"].play()

            th.point = Sprite.Rect(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()


class Kli(Base):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((0, 0, 12, 26)), group[2], pos=(292, 332), radius=2)

        th.group = group[0]
        th.particle_group = group[1]
        th.color = color_dict[5]
        th.collided = Invinc(180, 6)
        th.divided = Invinc(180, 4, th.reset_bullet)
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

                for bullet_info in bullet_type:
                    Sprite.Bullet(effective, "bullet", 16, th.color, bullet_info['angle'], (bullet_info['x'], bullet_info['y']), 4, bullet_cache["bullet"], th.group)

        sound_cache["fire"].play(maxtime=32)

    def free(th):
        th.bullet_timer += 1

        if th.bullet_timer == 10:
            for i in range(120, 466, 15):
                pos = (i, randint(345, 360))
                rands = choice([3, 6, 9, 12])

                Sprite.Item('char', uniform(1, 2), pos, th.particle_group, size=rands, color=color_dict[6])

            sound_cache["charge"].play()

        if th.bullet_timer >= 30 and th.bomb_bullets < 6:
            for i in range(120, 466, 15):
                Sprite.Bullet(effective, "bomb", -24, th.color, 0, (i, 0), 6, bullet_cache["bomb"], th.group)

            th.bomb_bullets += 1

            sound_cache["fire"].play(maxtime=32)

    def update(th):
        if th.divided.condition:
            th.free()

        th.image = Change.swivel(char_image.subsurface((0, 0, 12, 26)), char_image.subsurface((12, 0, 12, 26)), th.is_move_right, th.is_move_left)
        if th.is_move_left:
            th.x -= 8 if th.is_fast else 3
        if th.is_move_right:
            th.x += 8 if th.is_fast else 3
        th.x = clamp(th.x, window.left, window.right)
        th.y = 331 if th.is_fast else 332
        th.divided.update()
        th.collided.update()

        if th.is_shoot and th.bullets > 0:
            th.fire()
            Sprite.spawn_particles(th.particle_group, 2, th.rect.center, (4, 8), th.color)

            th.bullets -= 1

    def reset_bullet(th):
        th.bomb_bullets = 0
        th.bullet_timer = 0