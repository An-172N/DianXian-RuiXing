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
    def __init__(th, image: pg.Surface, turn_image: pg.Surface, hp: int, color: tuple, *group: pg.sprite.Group):
        super().__init__(image, group[2], turn_image=turn_image, pos=(292, 60))
        th.barrage_group = group[0]
        th.particle_group = group[1]
        th.bullet_group = group[3]
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
        super().__init__(char_image.subsurface((24, 0, 12, 26)), char_image.subsurface((36, 0, 12, 26)), 224, color_dict[1], *group)
        th.bullet_image = barrage_cache[(2, th.color)]
        th.power = True
        th.sd = tuple([th.fire] * 3 + [th.free, th.extend, th.final])

    def fire(th):
        if th.timer == 0:
            for i in range(0, 360, 15):
                pos = (th.x, th.y)
                Barrage(effective, 4, th.color, i, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def free(th):
        if th.timer == 0:
            speed = 5
            delay = 0
            for _ in range(8):
                for j in range(-30, 31, 30):
                    delay += 20
                    for k in (j - 180, j, 180 - delay):
                        delta = add(th.locate, (-th.x, -th.y))
                        angle = direct(*inverse(delta)) + k
                        Barrage(effective, speed, th.color, angle, (th.x, th.y), th.bullet_image, th.barrage_group, 3)
                speed -= 0.5
            sound_cache["fire"].play()

    def extend(th):
        if th.bullets < 10:
            for i in range(0 + th.timer * 7, 360 + th.timer * 7, 180):
                for j in range(0 + th.timer * 7, 360 + th.timer * 7, 90):
                    pos = (th.x + 32 * cos(radians(i)), th.y + 32 * sin(radians(i)))
                    Barrage(effective, 3.5, th.color, j, pos, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def final(th):
        if th.bullets < 24:
            delta = add(th.locate, (-th.x, -th.y))
            for i in (2, 1, -1, -2):
                angle = ((th.timer * 12) * i) + (direct(*inverse(delta)) + 180)
                pos = (th.x, th.y)
                Barrage(effective, 4, th.color, angle, pos, th.bullet_image, th.barrage_group, 3)
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
            image = barrage_cache[(2, color_dict[6])]
            for i in range(0, 360, 30):
                pos = (th.x + 48 * cos(radians(i)), th.y + 48 * sin(radians(i)))
                delta = add((th.x, th.y), inverse(pos))
                angle = direct(*inverse(delta))
                Barrage(effective, 3, color_dict[6], angle, pos, image, th.particle_group)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()
        delay = th.x
        th.x, th.y = vector((th.x, th.y), th.target_pos, 4)[0]
        th.swivel(th.x < delay, th.x > delay)


class Hro(Basic):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((48, 0, 12, 26)), char_image.subsurface((60, 0, 12, 26)), 256, color_dict[2], *group)
        th.flash = True
        th.bullet_image = barrage_cache[(0, th.color)]
        th.sd = tuple([th.fire] * 2 + [th.free] + [th.fire] * 3 + [th.extend] + [th.fire] * 4 + [th.free, th.extend])

    def fire(th):
        if th.timer % 6 == 0 and th.bullets < 3:
            pos = (th.x, th.y)
            for i in range(-30, 31, 30):
                delta = add((th.locate[0], th.locate[1]), inverse(pos))
                angle = direct(*inverse(delta)) + i
                Barrage(effective, 4, th.color, angle, pos, th.bullet_image, th.barrage_group, 2, rotate=True)
            th.bullets += 1
            sound_cache["fire"].play()

    def free(th):
        if th.bullets < 18:
            for i in (0, 1):
                dx1 = 120 if i else 465
                dx2 = 465 if i else 120
                start_pos = (dx1, 15)
                end_pos = (dx2, 345)
                current_pos, delta_vec = vector(start_pos, end_pos, th.bullets * 25)
                for j in range(45, 136, 90):
                    angle = direct(*inverse(delta_vec)) + j + (th.timer * -6)
                    Barrage(effective, 4, th.color, angle, current_pos, th.bullet_image, th.barrage_group, 2, rotate=True)
            th.bullets += 1
            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        if th.timer == 0:
            speed = 6
            for _ in range(6):
                for j in (150, 185, 220, 255, 292, 327, 365, 400, 435):
                    for k in range(0, 4):
                        pos = (j, 60)
                        delta = add((th.locate[0], th.locate[1] - 160), inverse(pos))
                        angle = direct(*inverse(delta)) + k * 90
                        Barrage(effective, speed, th.color, angle, pos, th.bullet_image, th.barrage_group, 2, rotate=True)
                speed -= 0.6
            sound_cache["fire"].play()

    def update(th):
        th.timer += 1
        if th.timer % 110 == 0:
            th.target_pos = (choice((150, 220, 292, 365)), choice((60, 120, 180, 240)))
            th.bullets = 0
            th.timer = 0
            th.can_shoot = True
        if th.timer % 91 == 0 and th.timer % 110 >= 91:
            th.choice = th.sd[th.index]
            th.index = (th.index + 1) if th.index < len(th.sd) - 1 else 0
            image = barrage_cache[(0, color_dict[6])]
            for i in range(0, 360, 120 if th.choice == th.fire else 90):
                pos = (th.x + 45 * cos(radians(i)), th.y + 45 * sin(radians(i)))
                delta = add((th.x, th.y), inverse(pos))
                angle = direct(*inverse(delta))
                Barrage(effective, 3, color_dict[6], angle, pos, image, th.particle_group, rotate=True)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot and th.timer < 91:
            th.choice()
        for barrage, hit_bullets in pg.sprite.groupcollide(th.barrage_group, th.bullet_group, True, False).items():
            for bullet in hit_bullets:
                if not hasattr(barrage, "is_die"):
                    barrage.is_die = False
                if not barrage.is_die:
                    if sound_cache['tick'].get_num_channels() < 2:
                        sound_cache['tick'].play()
                    if bullet.type == "bullet":
                        bullet.kill()
                    barrage.is_die = True
        delay = th.x
        th.x, th.y = vector((th.x, th.y), th.target_pos, 5)[0]
        th.swivel(th.x < delay, th.x > delay)


class Nre(Basic):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((72, 0, 12, 26)), char_image.subsurface((84, 0, 12, 26)), 288, color_dict[3], *group)
        th.power = True
        th.sd = (th.fire, th.free, th.fire, th.extend, th.fire, th.final, th.fire, th.last, th.extend, th.final, th.last)

    def fire(th):
        if th.timer == 0:
            for i in range(th.locate[0] - 35, th.locate[0] + 36, 23):
                line_barrage((i, 15), (i, 345), th.barrage_group, color_dict[6], color_dict[3])
            sound_cache["fire"].play()

    def free(th):
        if th.bullets < 16:
            current, target = (randint(120, 465), 15), (randint(120, 465), 345)
            line_barrage(current, target, th.barrage_group, color_dict[6], color_dict[3])
            th.bullets += 1
            if th.bullets % 3 == 0:
                sound_cache["fire"].play()

    def extend(th):
        if th.bullets < 8 and th.timer % 3 == 0:
            for j in (1, -1):
                current, target = (th.interval_locate[0] + th.bullets * j * 24, 15), ((th.interval_locate[0] + th.bullets * j * 24), 345)
                line_barrage(current, target, th.barrage_group, color_dict[6], color_dict[3])
            current, target = (120, (th.locate[1] - 13) - th.bullets * 24), (465, ((th.locate[1] - 13) - th.bullets * 24))
            line_barrage(current, target, th.barrage_group, color_dict[6], color_dict[3])
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def final(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            current, target = (220 + th.bullets * 25, 15), ((320 + th.bullets * 25), 345)
            line_barrage(current, target, th.barrage_group, color_dict[6], color_dict[3])
            if th.bullets < 6:
                for i in (120, 465):
                    current, target = (i, 15), (292 + th.bullets * choice([32, -32]), 345)
                    line_barrage(current, target, th.barrage_group, color_dict[6], color_dict[3])
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def last(th):
        if th.bullets < 20 and th.timer % 2 == 0:
            pos = (th.x + 478 * cos(radians(th.bullets * 18)), th.y + 478 * sin(radians(th.bullets * 18)))
            rands = (randint(120, 465), randint(15, 255))
            line_barrage(th.interval_pos, pos, th.barrage_group, color_dict[6], color_dict[3])
            for _ in range(3):
                pos = (rands[0] + 478 * cos(radians(th.bullets * 18)), rands[1] + 478 * sin(radians(th.bullets * 18)))
                line_barrage(rands, pos, th.barrage_group, color_dict[6], color_dict[3])
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
            th.choice = th.sd[th.index]
            th.index = (th.index + 1) if th.index < len(th.sd) - 1 else 0
        if th.timer % 100 >= 82 and th.timer % 82 == 0:
            image = particle_cache[(9, color_dict[6])]
            for _ in range(8):
                pos = (int(uniform(th.x - 48, th.x + 48)), th.y)
                delta = add((th.x, th.y), inverse(pos))
                angle = direct(*inverse(delta))
                Barrage(effective, 3, color_dict[6], angle, pos, image, th.particle_group)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()
        delay = th.x
        th.x, th.y = vector((th.x, th.y), th.target_pos, 6)[0]
        th.swivel(th.x < delay, th.x > delay)


class Qdi(Basic):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface((96, 0, 12, 26)), 128, color_dict[4], *group)
        th.bullet_image = barrage_cache[(2, th.color)]
        th.power = True

    def fire(th):
        if th.bullets < 6 and th.timer % 2 == 0:
            pos = (randint(120, 465), randint(15, 230))
            delta = add(th.locate, inverse(pos))
            angle = direct(*inverse(delta))
            Barrage(effective, 3.5, th.color, angle, pos, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def free(th):
        if th.timer == 0:
            for _ in range(64):
                angle = randint(0, 360)
                pos = (randint(120, 465), randint(15, 225))
                Barrage(effective, 4, th.color, angle, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def extend(th):
        if th.timer == 0:
            for _ in range(8):
                pos = (randint(120, 465), randint(15, 200))
                rands = randint(0, 30)
                for j in range(0 + rands, 360 + rands, 30):
                    speed = randint(2, 5)
                    Barrage(effective, speed, th.color, j, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def final(th):
        if 4 <= th.timer <= 12 and th.timer % 4 == 0:
            pos = (randint(120, 465), randint(15, 160))
            for _ in range(10):
                rands = randint(0, 60)
                for i in range(0 + rands, 360 + rands, 60):
                    speed = randint(2, 5)
                    Barrage(effective, speed, th.color, i, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def last(th):
        if th.timer == 0:
            bullets = choice([20, 24, 30, 40])
            pos = th.rect.center
            delta = add(th.locate, inverse(pos))
            angle = direct(*inverse(delta))
            end = randint(0 + int(angle), 360 + int(angle))
            for i in range(0 + int(angle), 360 + int(angle), 360 // bullets):
                fast_speed = uniform(6.0, 7.0)
                slow_speed = uniform(3.0, 4.0)
                fast_lose = uniform(0.2, 0.55)
                slow_lose = uniform(0.15, 0.3)
                for _ in range(8):
                    fast_speed -= fast_lose
                    slow_speed -= slow_lose
                    speed = fast_speed if i <= end else slow_speed
                    Barrage(effective, speed, th.color, i, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def count(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            for i in range(0, 360, 30):
                angle = i + 8 * th.bullets
                speed = randint(4, 6)
                Barrage(effective, speed, th.color, angle, th.rect.center, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play()

    def update(th):
        th.timer += 1
        if th.timer % 150 == 0:
            th.x, th.y = (randint(150, 435), randint(48, 96))
            th.bullets = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = choice([th.fire] * 12 + [th.free] * 2 + [th.extend, th.final, th.last, th.count])
        if th.timer % 150 >= 145:
            th.x += choice([-4, 4])
        if th.timer % 125 == 0 and th.timer % 150 >= 125:
            image = barrage_cache[(2, color_dict[6])]
            for _ in range(12):
                pos = (int(uniform(th.x - 48, th.x + 48)), int(uniform(th.y - 64, th.y + 64)))
                delta = add((th.x, th.y), inverse(pos))
                angle = direct(*inverse(delta))
                Barrage(effective, 3, color_dict[6], angle, pos, image, th.particle_group)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[1])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()


class Kli(Base):
    def __init__(th, *group: pg.sprite.Group):
        super().__init__(char_image.subsurface(0, 0, 12, 26), group[2], turn_image=char_image.subsurface(12, 0, 12, 26), pos=(292, 332))
        th.bullet_group = group[0]
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
        q = 1 * (th.power // 16)
        image = bullet_cache["bullet"]
        for i in range(0, p):
            for j in range(-q, q + 1, (q if th.power >= 16 else 1)):
                for k in (-1, 1):
                    dx = th.rect.centerx + 6 * k
                    dy = th.rect.top + (0 + i * 12)
                    angle = j * k
                    Bullet(effective, 16, th.color, angle, (dx, dy), 4, image, th.bullet_group, form="bullet", rotate=True)
        sound_cache["fire"].play(maxtime=32)

    def free(th):
        th.bullet_timer += 1
        if th.bullet_timer == 10:
            for i in range(120, 466, 15):
                pos = (i, randint(345, 360))
                rands = choice([3, 6, 9, 12])
                speed = uniform(1, 2)
                image = particle_cache[(rands, color_dict[6])]
                Barrage(effective, speed, th.color, 0, pos, image, th.particle_group, form='char')
            sound_cache["charge"].play()
        if th.bullet_timer >= 30 and th.bomb_bullets < 6:
            image = bullet_cache["bomb"]
            for i in range(120, 466, 15):
                Bullet(effective, -24, th.color, 0, (i, 0), 6, image, th.bullet_group, form="bomb")
            th.bomb_bullets += 1
            sound_cache["fire"].play(maxtime=32)

    def update(th):
        keys = pg.key.get_pressed()
        th.is_move_left = True if keys[pg.K_LEFT] else False
        th.is_move_right = True if keys[pg.K_RIGHT] else False
        th.is_shoot = False if keys[pg.K_z] else True
        th.is_fast = True if keys[pg.K_x] else False
        if keys[pg.K_SPACE]:
            th.divided.condition, th.power = bomb(th.divided.condition, th.power, 12)
        if th.divided.condition:
            th.free()
        th.swivel(th.is_move_right, th.is_move_left)
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