# (C)opyright 2026 An_172N
# 此代码遵循 GPLv3.0 协议

import json
import sys
import os
from datetime import datetime
from random import randint, choice, uniform, sample
from math import sin, cos, radians

import pygame as pg
from pygame.sprite import Group

from PRELOAD import *
from LOGIC import *

class One:
    def __init__(th):
        th.plane_group = Group()
        th.bullet_group = Group()
        th.brick_group = Group()
        th.item_group = Group()
        th.barrage_group = Group()
        th.particle_group = Group()
        th.is_pause = False
        th.is_summary = False
        th.is_talk = False
        th.is_save = False
        th.is_check = False
        th.is_level_load = False
        th.is_exit = False
        th.char = None
        th.text = None
        th.item_spawn_timer = 0
        th.total_point = 0
        th.combo_timer = 120
        th.combo = 0
        th.text_number = 0
        th.text_part = 0
        th.pop_timer = 0
        th.remaining_brick = []
        th.brick_ready = []

class Two:
    def __init__(th):
        th.is_run = False
        th.flash = 3
        th.unflash = 1
        th.score = 0
        th.flashed = 0
        th.total_point = 0
        th.stage = 1
        th.level = 1
        th.wait_load_timer = 0

class Log:
    def __init__(th):
        th.name = ''
        th.log = None
        th.files = get_files(f'{os.path.expanduser("~")}/Saved Games/DX00')
        th.index = 0
        th.total_files = len(th.files)

def score_summary(total_point, power, unflash, combo, numbers):
    return (
        total_point * 512 + unflash * 4096 +
        ((2 ** combo) if combo > 0 else 0) +
        ((numbers[0] * 16384) if numbers[1] == 6 else 0) +
        ((int(power / 32 * 8192)) if numbers[1] == 6 else 0)
    )

def combo_counter(timer, count, score, bonus, end):
    timer -= 1
    if timer <= 0:
        if count > 0:
            score += bonus
        count = 0
        timer = end

    return timer, count, score

class Basic(Base):
    def __init__(th, image, turn_image, hp, color, barrage_group, particle_group, brick_group):
        super().__init__(image, brick_group, turn_image, pos=(292, 60))
        th.barrage_group = barrage_group
        th.particle_group = particle_group
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
    def __init__(th, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((24, 0, 12, 26)), subsurface((36, 0, 12, 26)), 512, color_dict[1], *group)
        th.bullet_image = barrage_cache[(2, color_dict[6])]
        th.power = True
        th.sd = (th.fire,) * 3 + (th.free, th.extend, th.final)

    def fire(th):
        if th.timer == 0:
            for i in range(0, 360, 15):
                Barrage(effective, 4, i, th.rect.center, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def free(th):
        if th.timer == 0:
            speed = 5
            delay = 0
            for _ in range(8):
                for j in range(-30, 31, 30):
                    delay += 20
                    for k in (j - 180, j, 180 - delay):
                        angle = bearing(th.locate, th.rect.center) + k
                        Barrage(effective, speed, angle, (th.x, th.y), th.bullet_image, th.barrage_group, 3)
                speed -= 0.5
            sound_cache["fire"].play()

    def extend(th):
        if th.bullets < 10:
            for i in range(0 + th.timer * 7, 360 + th.timer * 7, 180):
                rad = radians(i)
                for j in range(0 + th.timer * 7, 360 + th.timer * 7, 90):
                    pos = th.x + 32 * cos(rad), th.y + 32 * sin(rad)
                    Barrage(effective, 3.5, j, pos, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(48 if th.bullets < 9 else 0))

    def final(th):
        if th.bullets < 24:
            for i in (2, 1, -1, -2):
                angle = th.timer * 12 * i + (bearing(th.locate, th.rect.center) + 180)
                Barrage(effective, 4, angle, th.rect.center, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(48 if th.bullets < 24 else 0))

    def update(th):
        th.timer += 1
        if th.timer % 120 == 0:
            rad = radians(randint(0, 360))
            th.target_pos = 292 + 50 * cos(rad), 110 + 50 * sin(rad)
            th.bullets = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = th.sd[th.index]
            th.index = (th.index + 1) if th.index < len(th.sd) - 1 else 0
        if th.timer % 99 == 0 and th.timer % 120 >= 99: 
            image = barrage_cache[(2, color_dict[6])]
            for i in range(0, 360, 30):
                rad2 = radians(i)
                pos = th.x + 48 * cos(rad2), th.y + 48 * sin(rad2)
                angle = bearing(th.rect.center, pos)
                Barrage(effective, 3, angle, pos, image, th.particle_group)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[6])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()
        delay = th.x
        th.x, th.y = vector((th.x, th.y), th.target_pos, 4)[0]
        th.swivel(th.x < delay, th.x > delay)

class Hro(Basic):
    def __init__(th, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((48, 0, 12, 26)), subsurface((60, 0, 12, 26)), 768, color_dict[2], *group)
        th.flash = True
        th.bullet_image = barrage_cache[(0, color_dict[6])]
        th.sd = (th.fire, th.fire, th.free) + (th.fire,) * 3 + (th.extend,) + (th.fire,) * 4 + (th.free, th.extend)

    def fire(th):
        if th.timer % 6 == 0 and th.bullets < 3:
            pos = th.rect.center
            for i in range(-30, 31, 30):
                angle = bearing(th.locate, pos) + i
                Barrage(effective, 4, angle, pos, th.bullet_image, th.barrage_group, 2, True)
            th.bullets += 1
            sound_cache["fire"].play(maxtime=(98 if th.bullets < 3 else 0))

    def free(th):
        if th.bullets < 18:
            for i in (0, 1):
                dx1 = 120 if i else 465
                dx2 = 465 if i else 120
                start_pos = dx1, 15
                end_pos = dx2, 345
                current_pos = vector(start_pos, end_pos, th.bullets * 25)[0]
                for j in range(45, 136, 90):
                    angle = bearing(end_pos, start_pos) + j + (th.timer * -6)
                    Barrage(effective, 4, angle, current_pos, th.bullet_image, th.barrage_group, 2, True)
            th.bullets += 1
            if th.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(48 if th.bullets < 18 else 0))

    def extend(th):
        if th.timer == 0:
            speed = 6
            for _ in range(6):
                for j in range(152, 468, 35):
                    for k in range(0, 4):
                        pos = j, 60
                        angle = bearing((th.locate[0], th.locate[1] -160), pos) + k * 90
                        Barrage(effective, speed, angle, pos, th.bullet_image, th.barrage_group, 2, True)
                speed -= 0.6
            sound_cache["fire"].play()

    def update(th):
        th.timer += 1
        if th.timer % 110 == 0:
            th.target_pos = choice((150, 220, 292, 365)), choice((60, 120, 180, 240))
            th.bullets = 0
            th.timer = 0
            th.can_shoot = True
        if th.timer % 91 == 0 and th.timer % 110 >= 91:
            th.choice = th.sd[th.index]
            th.index = (th.index + 1) if th.index < len(th.sd) - 1 else 0
            image = barrage_cache[(0, color_dict[6])]
            for i in range(0, 360, 120 if th.choice == th.fire else 90):
                rad = radians(i)
                pos = th.x + 45 * cos(rad), th.y + 45 * sin(rad)
                angle = bearing(th.rect.center, pos)
                Barrage(effective, 3, angle, pos, image, th.particle_group, rotate=True)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[6])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot and th.timer < 91:
            th.choice()
        delay = th.x
        th.x, th.y = vector((th.x, th.y), th.target_pos, 5)[0]
        th.swivel(th.x < delay, th.x > delay)

class Nre(Basic):
    def __init__(th, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((72, 0, 12, 26)), subsurface((84, 0, 12, 26)), 1024, color_dict[3], *group)
        th.power = True
        th.sd = th.fire, th.free, th.fire, th.extend, th.fire, th.final, th.fire, th.last, th.extend, th.final, th.last

    def fire(th):
        if th.timer == 0:
            for i in range(th.locate[0] - 35, th.locate[0] + 36, 23):
                line_barrage((i, 15), (i, 345), th.barrage_group)
            sound_cache["fire"].play()

    def free(th):
        if th.bullets < 16:
            current, target = (randint(120, 465), 15), (randint(120, 465), 345)
            line_barrage(current, target, th.barrage_group)
            th.bullets += 1
            if th.bullets % 3 == 0:
                sound_cache["fire"].play(maxtime=(48 if th.bullets < 15 else 0))

    def extend(th):
        if th.bullets < 8 and th.timer % 3 == 0:
            for j in (1, -1):
                x = th.interval_locate[0] + th.bullets * j * 24
                current, target = (x, 15), (x, 345)
                line_barrage(current, target, th.barrage_group)
            y = (th.locate[1] - 13) - th.bullets * 24
            current, target = (120, y), (465, y)
            line_barrage(current, target, th.barrage_group)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(98 if th.bullets < 8 else 0))

    def final(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            current, target = (220 + th.bullets * 25, 15), (320 + th.bullets * 25, 345)
            line_barrage(current, target, th.barrage_group)
            if th.bullets < 6:
                for i in (120, 465):
                    current, target = (i, 15), (292 + th.bullets * choice([32, -32]), 345)
                    line_barrage(current, target, th.barrage_group)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(65 if th.bullets < 12 else 0))

    def last(th):
        if th.bullets < 20 and th.timer % 2 == 0:
            rad = radians(th.bullets * 18)
            pos = th.x + 478 * cos(rad), th.y + 478 * sin(rad)
            rands = randint(120, 465), randint(15, 255)
            line_barrage(th.interval_pos, pos, th.barrage_group)
            for _ in range(3):
                pos = rands[0] + 478 * cos(rad), rands[1] + 478 * sin(rad)
                line_barrage(rands, pos, th.barrage_group)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(65 if th.bullets < 20 else 0))

    def update(th):
        th.timer += 1
        if th.timer % 100 == 0:
            th.target_pos = choice((150, 220, 292, 365, 435)), 60
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
                pos = randint(th.x - 48, th.x + 48), th.y
                angle = bearing(th.rect.center, pos)
                Barrage(effective, 3, angle, pos, image, th.particle_group)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[6])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()
        delay = th.x
        th.x, th.y = vector((th.x, th.y), th.target_pos, 6)[0]
        th.swivel(th.x < delay, th.x > delay)

class Qdi(Basic):
    def __init__(th, barrage_group, particle_group, brick_group):
        subsurface = char_image.subsurface
        group = barrage_group, particle_group, brick_group
        super().__init__(subsurface((96, 0, 12, 26)), subsurface((108, 0, 12, 26)), 128, color_dict[4], *group)
        th.bullet_image = barrage_cache[(2, color_dict[6])]
        th.power = True

    def fire(th):
        if th.bullets < 6 and th.timer % 2 == 0:
            pos = randint(120, 465), randint(15, 230)
            angle = bearing(th.locate, pos)
            Barrage(effective, 3.5, angle, pos, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(65 if th.bullets < 6 else 0))

    def free(th):
        if th.timer == 0:
            for _ in range(64):
                angle = randint(0, 360)
                pos = randint(120, 465), randint(15, 225)
                Barrage(effective, 4, angle, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def extend(th):
        if th.timer == 0:
            for _ in range(8):
                pos = randint(120, 465), randint(15, 200)
                rands = randint(0, 30)
                for j in range(0 + rands, 360 + rands, 30):
                    speed = randint(2, 5)
                    Barrage(effective, speed, j, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def final(th):
        if 4 <= th.timer <= 12 and th.timer % 4 == 0:
            pos = randint(120, 465), randint(15, 160)
            for _ in range(10):
                rands = randint(0, 60)
                for i in range(0 + rands, 360 + rands, 60):
                    speed = randint(2, 5)
                    Barrage(effective, speed, i, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def last(th):
        if th.timer == 0:
            bullets = choice((20, 24, 30, 40))
            pos = th.rect.center
            angle = int(bearing(th.locate, pos))
            end = randint(0 + angle, 360 + angle)
            for i in range(0 + angle, 360 + angle, 360 // bullets):
                fast_speed, slow_speed = uniform(6.0, 7.0), uniform(3.0, 4.0)
                fast_lose, slow_lose = uniform(0.2, 0.55), uniform(0.15, 0.3)
                for _ in range(8):
                    fast_speed -= fast_lose
                    slow_speed -= slow_lose
                    speed = fast_speed if i <= end else slow_speed
                    Barrage(effective, speed, i, pos, th.bullet_image, th.barrage_group, 3)
            sound_cache["fire"].play()

    def count(th):
        if th.bullets < 12 and th.timer % 2 == 0:
            for i in range(0, 360, 30):
                angle = i + 8 * th.bullets
                speed = randint(4, 6)
                Barrage(effective, speed, angle, th.rect.center, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(65 if th.bullets < 12 else 0))

    def what(th):
        if th.bullets < 8 and th.timer % 2 == 0:
            for i in range(90, 271, randint(5, 30)):
                pos = (120 + th.bullets * 44, th.rect.centery)
                Barrage(effective, randint(2, 4), i, pos, th.bullet_image, th.barrage_group, 3)
            th.bullets += 1
            if th.bullets % 2 == 0:
                sound_cache["fire"].play(maxtime=(65 if th.bullets < 8 else 0))

    def update(th):
        th.timer += 1
        if th.timer % 150 == 0:
            th.x, th.y = randint(150, 435), randint(48, 96)
            th.bullets = 0
            th.timer = 0
            th.can_shoot = True
            th.choice = choice((th.fire,) * 12 + (th.free,) * 2 + (th.extend, th.final, th.last, th.count, th.what))
        delay = th.x
        if th.timer % 150 >= 145:
            th.x += choice((-4, 4))
        th.swivel(th.x < delay, th.x > delay)
        if th.timer % 125 == 0 and th.timer % 150 >= 125:
            image = barrage_cache[(2, color_dict[6])]
            for _ in range(12):
                pos = randint(th.x - 48, th.x + 48), randint(th.y - 64, th.y + 64)
                angle = bearing(th.rect.center, pos)
                Barrage(effective, 3, angle, pos, image, th.particle_group)
            sound_cache["charge"].play()
            th.point = Base(particle_cache[(2, color_dict[6])], pos=(th.x, th.y))
        if th.point:
            pg.sprite.spritecollide(th.point, th.particle_group, True)
        if th.can_shoot:
            th.choice()

class Kli(Base):
    def __init__(th, bullet_group, particle_group, plane_group):
        subsurface = char_image.subsurface
        super().__init__(subsurface(0, 0, 12, 26), plane_group, subsurface(12, 0, 12, 26), pos=(292, 332), radius=1)
        th.bullet_group = bullet_group
        th.particle_group = particle_group
        th.color = color_dict[5]
        th.collided = Invinc(180, 6)
        th.divided = Invinc(180, 4, th.reset_bullet)
        th.bomb_bullets = 0
        th.bullet_timer = 0
        th.bullets = 0
        th.power = 0
        th.is_shoot = True
        th.is_fast = False

    def fire(th):
        p = 2 ** (th.power // 32)
        q = 1 * (th.power // 16)
        image = bullet_cache["bullet"]
        for _ in range(0, p):
            for j in range(-q, q + 1, (q if th.power >= 16 else 1)):
                for k in (-1, 1):
                    dx, dy = th.rect.centerx + 6 * k, th.rect.top
                    angle = j * k
                    Bullet(effective, 16, angle, (dx, dy), 4, image, th.bullet_group, form="bullet")
        sound_cache["fire"].play(maxtime=32)

    def free(th):
        th.bullet_timer += 1
        if th.bullet_timer == 10:
            for i in range(120, 466, 15):
                pos = i, randint(345, 360)
                rands = choice((3, 6, 9, 12))
                speed = uniform(1, 2)
                image = particle_cache[(rands, color_dict[6])]
                Barrage(effective, speed, 0, pos, image, th.particle_group, form='char')
            sound_cache["charge"].play()
        if th.bullet_timer >= 30 and th.bomb_bullets < 8:
            image = bullet_cache["bomb"]
            for i in range(120, 466, 15):
                Bullet(effective, -24, 0, (i, 0), 8, image, th.bullet_group, form="bomb")
            th.bomb_bullets += 1
            sound_cache["fire"].play(maxtime=32)

    def update(th):
        keys = pg.key.get_pressed()
        x = th.x
        if keys[pg.K_LEFT]:
            th.x -= 8 if th.is_fast else 3
        if keys[pg.K_RIGHT]:
            th.x += 8 if th.is_fast else 3
        th.is_shoot = False if keys[pg.K_z] else True
        th.is_fast = True if keys[pg.K_x] else False
        if keys[pg.K_SPACE]:
            th.divided.condition, th.power = one_shot(th.divided.condition, th.power, 12)
        if th.divided.condition:
            th.free()
        th.swivel(th.x > x, th.x < x)
        th.x = clamp(th.x, window.left, window.right)
        th.y = 331 if th.is_fast else 332
        th.divided.update()
        th.collided.update()
        if th.is_shoot and th.bullets > 0:
            th.fire()
            spawn_particles(th.particle_group, 2, th.rect.center, (4, 8), th.color)
            th.bullets -= 1

    def reset_bullet(th):
        th.bomb_bullets = 0
        th.bullet_timer = 0

    def visitable(th):
        return th.collided.visitable and th.divided.visitable

    def in_invinc(th):
        return not th.collided.condition and not th.divided.condition

def load_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        log.log = f.readline().split(',')

def spawn_barrage(group, power, type, spawn_pos, locate):
    index = two.stage - 1
    if uniform(0, 1) <= rank[index] + power / 1000:
        (
            lambda: circle_barrage(type, spawn_pos, locate, group),
            lambda: polygon_barrage(type, spawn_pos, locate, group),
            lambda: line_barrage((randint(120, 465), 15), (locate[0] + randint(-64, 64), 345), group),
            lambda: point_barrage(type, locate, group)
        )[index]()

def brick_blast(group, stage, color, pos):
    if color == color_dict[6]:
        (
            lambda: circle_brick(group, pos),
            lambda: polygon_brick(group, pos),
            lambda: line_brick(group, pos),
            lambda: point_brick(group)
        )[stage - 1]()

def sprite_loader():
    stage, level = two.stage, two.level
    if level == 6:
        one.char = choose_human()
        one.text = json.loads(asset(f"ASSET/JSON/{stage}.json").decode('utf-8'))
    else:
        process_lines(asset(f"ASSET/STAGE/{stage}-{level}.stg").decode('ascii'), load_brick, color_dict[stage], 4, (127, 22), (15, 15))
        choose_brick(one.brick_ready, (stage, level), 4, 1)

def choose_human():
    return (
        Ono,
        Hro,
        Nre,
        Qdi
    )[two.stage - 1](one.barrage_group, one.particle_group, one.brick_group)

def pop_bricks(remaining_brick, brick_ready, wait_load_timer, brick_group):
    if wait_load_timer >= 30 and wait_load_timer % 30 == 0:
        if not remaining_brick:
            remaining_brick = list(range(len(brick_ready)))
        if remaining_brick:
            size = len(remaining_brick) if wait_load_timer == 90 else min(len(brick_ready) // 3, len(remaining_brick))
            choose_brick = sample(remaining_brick, size)
            for i in choose_brick:
                brick_group.add(brick_ready[i])
            remaining_brick = [i for i in remaining_brick if i not in choose_brick]
    wait_load_timer += 1

    return wait_load_timer

def close_summary():
    two.wait_load_timer = 0
    one.is_level_load = True
    one.pop_timer = 0
    if two.level == 6:
        one.is_talk = True

def fade_surface(alpha, timer, is_exit, surface, screen):
    if is_exit:
        if timer % 30 == 0 and alpha < 255:
            alpha += 85
        timer -= 1
        surface.set_alpha(alpha)
        screen.blit(surface)
        if timer < -30:
            sys.exit()
    elif alpha > 0 and not is_exit:
        if timer % 30 == 0:
            alpha -= 85
        timer += 1
        surface.set_alpha(alpha)
        screen.blit(surface)

    return alpha, timer

def save_file(name, score, total_point, flashed, flash, numbers):
    stage, level = numbers
    name = name.translate(str.maketrans('!<>:"/\\|?*,', '___________'))
    time = (datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H-%M-%S'))
    rate = calculate_item_rate(total_point, stage <= 3)
    content = f"{name},{score},{f'{get_stage(stage)} - {level}'},{rate},{flashed},{time[0]},{flash}"
    record_file(f'{os.path.expanduser("~")}/Saved Games/DX00', f'{name}_{time[0]}_{time[1]}.dx00', content)

def calculate_item_rate(number, condition):
    return f"{(number / (153 if condition else 61) * 100):.2f} %"

def line_brick(group, pos):
    for _ in range(12):
        rands = choice((24, 48, 80))
        angle = 15 * randint(0, 11)
        start, end = coordinate(pos, angle, rands), coordinate(pos, angle - 180, rands)
        LineBullet(4, start, end, color_dict[5], color_dict[9], group)

def circle_brick(group, pos):
    image = bullet_cache["bullet"]
    delay = randint(0, 12)
    for i in range(0 + delay, 360 + delay, 12):
        Bullet(effective, 16, i, pos, 4, image, group, "bullet", True).update()

def polygon_brick(group, pos):
    image = bullet_cache["bullet"]
    for i in (-1, 1):
        for angle in range(-30, -91, -60):
            angle = angle * i
            Bullet(effective, 16, angle, pos, 4, image, group, "bullet-cross", True)

def point_brick(group):
    image = bullet_cache["bullet"]
    for _ in range(24):
        pos = randint(120, 465), randint(15, 320)
        angle = randint(0, 360)
        Bullet(effective, 16, angle, pos, 4, image, group, "bullet", True)

def load_brick(row, line, color, hp, size, interval):
    for i in range(len(line)):
        if line[i] != 'o':
            shape = int(line[i])
            pos = size[0] + i * interval[0], size[1] + row * interval[1]
            image = brick_cache[(shape, color)]
            one.brick_ready.append(Brick(shape, hp, color, pos, image))

def choose_brick(group, numbers, power, flash):
    choose_power = sample(range(len(group)), power + numbers[0] + numbers[1])
    choose_flash = sample(range(len(group)), flash)
    choose_white = sample(range(len(group)), 6)
    for i in choose_power:
        group[i].power = True
    for i in choose_flash:
        group[i].flash = True
    for i in choose_white:
        group[i].image = brick_cache[(group[i].type, color_dict[6])]
        group[i].color = color_dict[6]

def circle_barrage(type, pos, locate, group):
    angle = bearing(locate, pos)
    image = barrage_cache[(type, color_dict[6])]
    Barrage(effective, 3, angle, pos, image, group, 3)

def polygon_barrage(type, pos, locate, group):
    image = barrage_cache[(type, color_dict[6])]
    for i in range(locate[0] - 32, locate[0] + 33, 64):
        angle = bearing((i, locate[1]), pos)
        Barrage(effective, 3, angle, pos, image, group, 2, True)

def line_barrage(current, target, group):
    color = color_dict[6], color_dict[3]
    image = particle_cache[(3, color[0])]
    start = current
    count = 0
    while True:
        if not effective.collidepoint(current):
            break
        if 327 < current[1] < 336 or current == start:
            Line(color[0], color[1], current, target, count, image, group)
        if math.dist(current, target) < 1e-6:
            break
        current = vector(current, target, 3)[0]
        count += 1

def point_barrage(type, locate, group):
    image = barrage_cache[(type, color_dict[6])]
    for _ in range(3):
        pos = randint(120, 465), randint(15, 225)
        angle = bearing(locate, pos)
        Barrage(effective, 4, angle, pos, image, group, 3)

def spawn_particles(group, size, pos, speeds, color1, color2=None):
    rands = randint(0, 60)
    for i in range(0 + rands, 360 + rands, 60):
        color = color1 if color2 is None else choice((color1, color2))
        speed = uniform(speeds[0], speeds[1])
        image = particle_cache[(size, color)]
        Barrage(effective, speed, i, pos, image, group)

class Barrage(Base):
    def __init__(th, effective, speed, angle, pos, image, group, radius=0, rotate=False, form=None):
        super().__init__(image, group, None, form, angle, pos, radius, rotate)
        th.effective = effective
        th.speed = speed

    def update(th):
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)
        if getattr(th, "type", None) == "char":
            th.speed -= 0.1
            if th.speed < -4:
                th.speed = -4
        if not th.effective.collidepoint(th.rect.center):
            th.kill()

class Bullet(Base):
    def __init__(th, effective, speed, angle, pos, damage, image, group, form=None, rotate=False):
        super().__init__(image, group, None, form, angle, pos, rotate=rotate)
        th.effective = effective
        th.speed = speed
        th.damage = damage

    def update(th):
        rad = radians(th.angle)
        sin_, cos_ = sin(rad), cos(rad)
        th.x, th.y = th.x - (sin_ * th.speed), th.y - (cos_ * th.speed)
        if not th.effective.collidepoint(th.rect.center):
            th.kill()

class Text(Base):
    def __init__(th, pos, kill_times, speed, text, color, target_color, group):
        super().__init__(font.render(text, False, color), group, pos=pos)
        th.text = text
        th.color = color
        th.target_color = target_color
        th.kill_times = kill_times
        th.speed = speed
        th.timer = 0
        sound_cache["charge"].play(maxtime=128)

    def update(th):
        th.timer += 1
        th.y -= th.speed
        if th.timer >= th.kill_times[1]:
            th.kill()
        elif th.timer >= th.kill_times[0] and th.color != th.target_color:
            th.color = th.target_color
            th.image = font.render(th.text, False, th.color)

class Brick(Base):
    def __init__(th, form, hp, color, pos, image):
        super().__init__(image, form=form, pos=pos)
        th.color = color
        th.hp = hp
        th.power = False
        th.flash = False
        th.is_die = False

class Item(Base):
    def __init__(th, type, speed, pos, group):
        super().__init__(item_cache[type], group, form=type, pos=pos)
        th.speed = speed

    def update(th):
        th.y -= th.speed
        th.speed -= 0.1
        if th.speed < -2:
            th.speed = -2
        if th.y >= 360:
            th.kill()

class Line(Base):
    def __init__(th, color, target_color, pos, target, count, image, group):
        super().__init__(image, group, pos=pos, radius=1.5)
        th.color = color
        th.target_color = target_color
        th.start_pos = pos
        th.count = count
        if not count:
            th.target_pos = target
        th.timer = 0

    def draw_line(th):
        if not th.count:
            pg.draw.line(screen, th.color, th.start_pos, th.target_pos, 3)

    def update(th):
        th.timer += 1
        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            th.color = th.target_color

class LineBullet(Base):
    def __init__(th, damage, start, end, color, target_color, group):
        super().__init__(particle_cache[(2, color_dict[4])], group, pos=(0, 0), form="line")
        th.damage = damage
        th.color = color
        th.start_pos = start
        th.end_pos = end
        th.target_color = target_color
        th.timer = 0

    def draw_bullet(th):
        pg.draw.line(screen, th.color, th.start_pos, th.end_pos, 2)

    def update(th):
        th.timer += 1
        if th.timer >= 68:
            th.kill()
        elif th.timer >= 45 and th.color != th.target_color:
            th.color = th.target_color

def reset(thorough=True):
    one.__init__()
    if thorough:
        two.__init__()
        log.__init__()
    major.__init__(one.bullet_group, one.particle_group, one.plane_group)

def situation(clock):
    color = color_dict[6]
    text = (
        f"{two.score:9d}",
        f"{int(clock.get_fps()):9d}",
        f"{major.power:02d}  ,  {major.bullets:02d}",
        f"{two.flash:02d}",
        f"{one.combo:02d}  ,  {one.total_point:02d}"
    )
    for info in (
        (text[0], (39, 25)),
        (text[1], (39, 50)),
        (text[2], (39, 270)),
        (text[3], (39, 295)),
        (text[4], (39, 320)),
    ):
        screen.blit(font.render(info[0], False, color), info[1])

def pause_menu():
    title = "休息ing"
    text = ("Esc 休息好了", "Del 不爬了") if one.pop_timer >= 60 else ("", "")
    half_menu(title, text, shortly=one.pop_timer == 60)

def load_menu():
    title = "这一站是————"
    text = (f"Stage {get_stage(two.stage)} - {two.level}!!", "START!!!!")
    half_menu(title, text)

def talk_menu():
    try:
        text = one.text[f"{one.text_part}"][f"{one.text_number}"]
        human = text["char"]
        content = (text["1"], text["2"] if "2" in text else '')
        half_menu(human, content, (0, 6, 12))
    except KeyError:
        one.is_talk = False

def summary_menu():
    hit = 'Hit Z Key.' if two.level <= 5 and one.pop_timer >= 60 else ''
    stage = f"Stage {get_stage(two.stage)} - {two.level} Clear! {hit}"
    text = (
        f"得点 {one.total_point} * 512 = {one.total_point * 512}",
        f"无闪 {two.unflash} * 4096 = {two.unflash * 4096}",
        f"面数 {two.stage} * 16384 = {two.stage * 16384}",
        f"形力 {major.power} / 32 * 8192 = {int(major.power / 32 * 8192)}",
    )
    key = "Z 继续",
    if two.level <= 5:
        half_menu(stage, (text[0], text[1]), shortly=one.pop_timer == 60)
    else:
        full_menu(stage, text, key, stage_title[two.stage - 1])

def start_menu(version: str, title: str):
    other = "(C)opyright 2026 An_172N"
    text = f"Ver {version}",
    climb = "Z 爬山" if two.stage < 4 else "Z 下山"
    wood = "C 日志" if log.total_files > 0 else "C 木鱼"
    key = "Q 拜拜", wood, climb
    full_menu(title, text, key, other)

def save_menu():
    title = "爬山日志"
    name = f"{f'谢谢 {log.name} 的帮助' if one.pop_timer >= 60 else ''}"
    rate = calculate_item_rate(two.total_point, two.stage <= 3)
    date = datetime.now().strftime('%Y-%m-%d')
    text = get_logs(date, two.score, f"{get_stage(two.stage)} - {two.level}", rate, two.flashed, two.flash)
    key = "Esc 算了", "Ent 记录"
    keys = pg.key.get_pressed()
    shortly = one.pop_timer == 60 or (one.pop_timer >= 60 and any(keys[i] for i in range(len(keys))))
    full_menu(title, text, key, name, shortly=shortly)

def check_menu():
    try:
        if one.pop_timer == 0:
            load_file(log.files[log.index])
        logs = log.log
        title = f"爬山日志簿第 {log.total_files - log.index} / {log.total_files} 页"
        text = get_logs(logs[5], logs[1], logs[2], logs[3], logs[4], int(logs[6]))
        key = "Esc 合上", "Del 丢掉", "<-> 翻页"
        full_menu(title, text, key, f"谢谢 {logs[0]} 的帮助")
    except:
        one.is_check = False

def full_menu(title, texts, keys, other, interval=(0, 30, 60), shortly=False):
    color = color_dict[6]
    group = (
        (
            (font.render(title, False, color), (8, 10)),
            (font.render(other, False, color), (8, 305))
        ),
        tuple((font.render(texts[i], False, color), (8, 60 + 25 * i)) for i in range(len(texts))),
        tuple((font.render(keys[i], False, color), (275, 270 - 50 * i)) for i in range(len(keys)))
    )
    if one.pop_timer == interval[0]:
        picture[0].fill(color_dict[8])
    animate_pop(picture[0], group, one.pop_timer, interval, shortly)
    screen.blit(picture[0], (120, 15))
    if one.pop_timer == interval[2]:
        sound_cache["pick"].play()
    if one.pop_timer < interval[2] + 1:
        one.pop_timer += 1

def half_menu(title, texts, interval=(0, 30, 60), shortly=False):
    color = color_dict[6]
    group = (
        ((font.render(title, False, color), (8, 10)),),
        ((font.render(texts[0], False, color), (8, 60)),),
        ((font.render(texts[1], False, color), (8, 85)),)
    )

    if one.pop_timer == interval[0]:
        picture[0].fill(color_dict[8])
    source = picture[0].subsurface((0, 0, 345, 110))
    animate_pop(source, group, one.pop_timer, interval, shortly)
    screen.blit(source, (120, 15))
    if one.pop_timer == interval[2]:
        sound_cache["pick"].play()
    if one.pop_timer < interval[2] + 1:
        one.pop_timer += 1

def summary_logic():
    two.score += score_summary(one.total_point, major.power, two.unflash, one.combo, (two.stage, two.level))
    one.is_summary = False
    one.pop_timer = 0

def level_logic():
    if two.stage >= 3 and two.level == 6:
        one.is_save = True
    else:
        power = major.power
        one.is_save = False
        reset(False)
        major.power = power
        two.stage, two.level = carry(two.stage, two.level, 1, 6)
        two.unflash += 1

def item_collide():
    for item in pg.sprite.spritecollide(major, one.item_group, True):
        one.combo_timer = 120
        major.bullets = clamp(major.bullets + 1, 0, 3)
        if item.type in ('flash', 'power'):
            if item.type == "power":
                power = major.power
                major.power = clamp(major.power + 1, 0, 32)
                if power < 32 and major.power % 16 == 0:
                    Text(major.rect.midtop, (45, 60), 0.5, "Power UP", color_dict[6], color_dict[5], one.particle_group)
                else:
                    sound_cache["pick"].play()
            else:
                two.flash += 1
                Text(major.rect.midtop, (45, 60), 0.5, "Extend", color_dict[6], color_dict[2], one.particle_group)
            one.combo += 1
            one.total_point += 1
            two.total_point += 1
        else:
            sound_cache["charge"].play(maxtime=24)

def barrage_collide():
    for barrage in pg.sprite.spritecollide(major, one.barrage_group, False, collide_sprite):
        if (two.stage == 3 and barrage.color != color_dict[6]) or two.stage != 3:
            if major.in_invinc():
                major.collided.condition = True
                two.unflash = 0
                two.flash -= 1
                two.flashed += 1
                if two.flash == 0:
                    one.is_save = True
                spawn_particles(one.particle_group, 9, major.rect.center, (10, 16), color_dict[5], color_dict[6])
                sound_cache["fire"].play()
            barrage.kill()

def bullet_collide():
    count = 0
    for bullet, hit_bricks in pg.sprite.groupcollide(one.bullet_group, one.brick_group, False, False, collide_sprite).items():
        for brick in hit_bricks:
            rect = brick.rect
            count += 1
            if brick.hp > 0:
                two.score += 64
                brick.hp -= bullet.damage
                if brick.hp > 0 and count < 2:
                    spawn_particles(one.particle_group, 2, rect.center, (4, 8), brick.color, color_dict[6])
                    sound_cache["tick"].play()
            if brick.hp <= 0:
                if not brick.is_die:
                    if hasattr(brick, "free"):
                        one.text_part += 1
                        one.text_number = 0
                        one.is_talk = True
                        one.pop_timer = 0
                        one.particle_group.empty()
                        for _ in range(8):
                            spawn_particles(one.particle_group, 2, rect.center, (4, 8), brick.color, color_dict[6])
                    else:
                        spawn_barrage(one.barrage_group, major.power, brick.type, rect.center, major.rect.center)
                        spawn_particles(one.particle_group, 2, rect.center, (4, 8), brick.color, color_dict[6])
                    sound_cache["fire"].play()
                    if getattr(brick, "power", None):
                        Item("power", 2.5, rect.center, one.item_group)
                    if getattr(brick, "flash", None):
                        Item("flash", 2.5, rect.center, one.item_group)
                    brick_blast(one.bullet_group, two.stage, brick.color, rect.center)
                    brick.kill()
                brick.is_die = True
            if bullet.type in ("bullet", "bomb"):
                bullet.kill()
    if isinstance(one.char, Hro):
        for barrage, hit_bullets in pg.sprite.groupcollide(one.barrage_group, one.bullet_group, True, False).items():
            for bullet in hit_bullets:
                if not hasattr(barrage, "is_die"):
                    barrage.is_die = False
                if not barrage.is_die:
                    sound_cache['tick'].play()
                    if bullet.type == "bullet":
                        bullet.kill()
                    barrage.is_die = True

def key_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if one.pop_timer >= 60:
                if one.is_check and event.key in keydown_check_dict:
                    keydown_check_dict[event.key]()
                    one.pop_timer = 0
                    sound_cache["pick"].play()
                elif not two.is_run and not one.is_check and not one.is_exit and event.key in keydown_start_dict:
                    sound_cache["pick"].play()
                    keydown_start_dict[event.key]()
                elif one.is_save:
                    if event.key in keydown_over_dict:
                        keydown_over_dict[event.key]()
                    else:
                        log.name = (log.name + event.unicode)[:8]
                    sound_cache["pick"].play()
                elif one.is_pause and event.key in keydown_pause_dict:
                    keydown_pause_dict[event.key]()
                    one.pop_timer = 0
                    sound_cache["pick"].play()
                elif one.is_summary and event.key == pg.K_z:
                    summary_logic()
                    level_logic()
                    sound_cache["pick"].play()
            elif one.is_talk and not one.is_pause and event.key in keydown_talk_dict and one.pop_timer >= 12:
                keydown_talk_dict[event.key]()
                one.pop_timer = 0
                sound_cache["pick"].play()
            elif not one.is_summary and one.is_level_load and not one.is_talk and not one.is_pause and event.key == pg.K_ESCAPE:
                one.is_pause = True
                one.pop_timer = 0
                sound_cache["pick"].play()

def display(clock, version, title):
    if two.is_run:
        screen.blit(picture[two.stage], (120, 15))
        for bullet in one.bullet_group:
            if hasattr(bullet, "start_pos"):
                bullet.draw_bullet()
            else:
                screen.blit(bullet.image, bullet.rect)
        if major.visitable() and one.is_level_load:
            one.plane_group.draw(screen)
        one.brick_group.draw(screen)
        one.item_group.draw(screen)
        one.particle_group.draw(screen)
        if two.stage == 3:
            for line in one.barrage_group:
                line.draw_line()
        else:
            one.barrage_group.draw(screen)
    if one.is_check: check_menu()
    elif not two.is_run: start_menu(version, title)
    elif one.is_pause: pause_menu()
    elif not one.is_level_load: load_menu()
    elif one.is_talk: talk_menu()
    elif one.is_summary: summary_menu()
    elif one.is_save: save_menu()
    screen.blit(picture[5])
    situation(clock)

def update(clock, args, version, title):
    two.stage = clamp(args[0], 1, 4)
    two.level = clamp(args[1], 1, 6)
    two.flash = clamp(args[2], 1, 80)
    major.power = clamp(args[3], 0, 32)
    black_surface = pg.Surface((480, 360)).convert()
    alpha = 255
    timer = 0
    for info in (
        ("分", (9, 25)),
        ("刷", (9, 50)),
        ('形', (9, 270)),
        ('闪', (9, 295)),
        ('连', (9, 320))
    ):
        picture[5].blit(font.render(info[0], False, color_dict[6]), info[1])
    picture[5].set_clip(window)
    picture[5].fill((0, 0, 0, 0))
    while True:
        key_event()
        if two.is_run and not one.is_save and not one.is_pause:
            if not one.is_summary and not one.is_talk and one.is_level_load:
                if hasattr(one.char, "locate"):
                    one.char.locate = major.rect.center
                one.item_spawn_timer += 1
                if one.item_spawn_timer >= 45 and len(one.brick_group) > 0:
                    Item("fire", -2, (randint(120, 465), 10), one.item_group)
                    one.item_spawn_timer = 0
                if one.combo_timer <= 1 and one.combo > 0:
                    Text(major.rect.midtop, (45, 60), 0.5, f"{2 ** one.combo}", color_dict[6], color_dict[7], one.particle_group)
                one.combo_timer, one.combo, two.score = combo_counter(one.combo_timer, one.combo, two.score, 2 ** one.combo, 120)
                one.plane_group.update()
                one.bullet_group.update()
                one.barrage_group.update()
                one.item_group.update()
                one.particle_group.update()
                one.brick_group.update()
                barrage_collide()
                bullet_collide()
                item_collide()
                if len(one.brick_group) == 0 and len(one.item_group) == 0 and not one.is_talk:
                    one.is_summary = True
            if not one.is_level_load:
                if two.wait_load_timer <= 90:
                    if two.wait_load_timer == 0:
                        sprite_loader()
                    two.wait_load_timer = pop_bricks(one.remaining_brick, one.brick_ready, two.wait_load_timer, one.brick_group)
                else:
                    close_summary()
        display(clock, version, title)
        alpha, timer = fade_surface(alpha, timer, one.is_exit, black_surface, screen)
        pg.display.flip()
        clock.tick(60)

one = One()
two = Two()
log = Log()
major = Kli(one.bullet_group, one.particle_group, one.plane_group)

keydown_talk_dict = {
    pg.K_z: lambda: setattr(one, "text_number", one.text_number + 1),
    pg.K_x: lambda: setattr(one, "is_talk", False)
}

keydown_pause_dict = {
    pg.K_ESCAPE: lambda: setattr(one, "is_pause", False),
    pg.K_DELETE: lambda: reset()
}

keydown_start_dict = {
    pg.K_z: lambda: (setattr(two, "is_run", True), setattr(one, "pop_timer", 0)),
    pg.K_q: lambda: setattr(one, "is_exit", True),
    pg.K_c: lambda: (setattr(one, "is_check", True), setattr(one, "pop_timer", 0)) if log.total_files > 0 else None
}

keydown_over_dict = {
    pg.K_RETURN: lambda: (
        save_file(log.name, two.score, two.total_point, two.flashed, two.flash, (two.stage, two.level)),
        reset()
    ),
    pg.K_ESCAPE: lambda: reset(),
    pg.K_BACKSPACE: lambda: setattr(log, "name", log.name[:-1])
}

keydown_check_dict = {
    pg.K_DELETE: lambda: (os.remove(log.files[log.index]), log.__init__()),
    pg.K_ESCAPE: lambda: (setattr(one, "is_check", False), setattr(log, "index", 0)),
    pg.K_LEFT: lambda: setattr(log, "index", (log.index - 1) if log.index > 0 else log.total_files - 1),
    pg.K_RIGHT: lambda: setattr(log, "index", (log.index + 1) if log.index < log.total_files - 1 else 0)
}