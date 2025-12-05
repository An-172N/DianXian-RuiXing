import random as rand
import itertools
import math

import FUNC
import SCRIPT.DICT
import SCRIPT.VARIABLE as VARIABLE

from SCRIPT.LOGIC.FRIEND.BASE import Base
from SCRIPT.LOGIC.SPRITE import ITEM
from SCRIPT.LOGIC.PROCESS import STAGE


def spwn_blt() -> None:
    if (VARIABLE.can_shoot
        and VARIABLE.shoot_cnt > 0):
        p = 2 ** (VARIABLE.s_power // 32)
        q = 2 ** (VARIABLE.s_power // 16)

        for i, j in itertools.product(range(0, p), range(-q, q + 1, q)):
            VARIABLE.main_char.bomb.fire(
                0 + i * 10,
                0 + i * 12,
                j
            )

        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 60):
            spr = Base((2, 2, 0), VARIABLE.main_char.clr, 1)
            spr.spd = rand.randint(6, 10)
            spr.rect.center = VARIABLE.main_char.rect.center
            spr.curr_ang = i
            VARIABLE.ptcl_grp.add(spr)

        VARIABLE.shoot_cnt -= 1


def single_bomb() -> None:
    if (not VARIABLE.is_sdivide and
        VARIABLE.s_power >= 16):
        VARIABLE.s_power -= 16
        VARIABLE.is_sdivide = True


def blt_coll(src, tar) -> None:
    if src.type == "blt":
        if getattr(tar, 'is_die', False):
            src.kill()
            return

    tar.hp -= src.dmg
    VARIABLE.sc += 64

    if tar.hp <= 0:
        tar.is_die = True
        tar_pos = (tar.rect.centerx, tar.rect.centery)

        if hasattr(tar, "bomb"):
            STAGE.shhm_lose()

        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 60):
            spr = Base((2, 2, 0), tar.clr, 1)
            spr.spd = rand.randint(6, 10)
            spr.rect.center = tar_pos
            spr.curr_ang = i
            VARIABLE.ptcl_grp.add(spr)
            
        ITEM.item_spwn(tar_pos)
        brc_death(tar)
            
        tar.kill()

    if src.type == "blt":
        src.kill()


def item_coll(src) -> None:
    VARIABLE.bw_ctr = 90
    VARIABLE.ttl_s_power += 1
    VARIABLE.stg_ttl_s_power += 1
    if VARIABLE.shoot_cnt <= 7:
        VARIABLE.shoot_cnt += 1

    if src.type == 1:
        if VARIABLE.s_power < 32:
            VARIABLE.s_power += 1
        VARIABLE.comb += 1
    elif src.type == 2:
        VARIABLE.player += 1
        VARIABLE.comb += 1

    src.kill()


def brc_death(brc) -> None:
    if brc.clr == SCRIPT.DICT.clr_dict[6]:
        proc_dict = {
            0: polygon_brc,
            1: line_brc,
            2: circle_brc
        }

        proc_dict[brc.shape](
            Base,
            brc,
            VARIABLE.blt_grp,
            16
        )

    difficulty = FUNC.Calculate.fibonacci(
        0,
        1,
        VARIABLE.stage + 1
    ) / 100
    if rand.random() <= 0.25 + difficulty:
        brg_dict = {
            0: polygon_brg,
            1: line_brg,
            2: circle_brg
        }
        
        brg_dict[brc.shape](brc)
        

def circle_brg(brc) -> None:
    char = VARIABLE.main_char
    spr = Base((9, 9, 0), brc.clr, brc.shape)
    spr.spd = 2
    spr.rect.center = brc.rect.center
    x1 = char.rect.centerx
    x2 = spr.rect.centerx
    y1 = char.rect.centery
    y2 = spr.rect.centery
    two_pt = FUNC.Calculate.delta_tuple((x1, y1, 0), (x2, y2, 0))
    spr.curr_ang = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
    VARIABLE.brg_grp.add(spr)


def polygon_brg(brc) -> None:
    char = VARIABLE.main_char
    for i in range(char.rect.centerx - 32, char.rect.centerx + 33, 64):
        spr = Base((9, 9, 0), brc.clr, brc.shape)
        spr.spd = 2.5
        spr.rect.center = brc.rect.center
        x2 = spr.rect.centerx
        y1 = char.rect.centery
        y2 = spr.rect.centery
        two_pt = FUNC.Calculate.delta_tuple((i, y1, 0), (x2, y2, 0))
        spr.curr_ang = math.degrees(math.atan2(-two_pt[0], -two_pt[1]))
        VARIABLE.brg_grp.add(spr)


def line_brg(_) -> None:
    char = VARIABLE.main_char
    char_x = char.rect.centerx
    char_y = char.rect.centery
    start_pos = (rand.randint(100, 480), 0, 0)
    end_pos = (char_x, char_y, 0)

    dpos = FUNC.Calculate.delta_tuple(end_pos, start_pos)
    distance = math.hypot(dpos[0], dpos[1])
                
    spr = Base((2, distance, 0), (255, 255, 255), 1)
    spr.spd = 0
    x = start_pos[0] + dpos[0] / 2
    y = start_pos[1] + dpos[1] / 2
    spr.rect.center = (x, y)
    spr.curr_ang = math.degrees(math.atan2(-dpos[0], -dpos[1]))
    spr.update()
    VARIABLE.brg_grp.add(spr)


def circle_brc(spr, src, spr_grp, spd) -> None:
    rands = rand.randint(0, 45)

    for i in range(0 + rands, 360 + rands, 15):
        curr_spr = spr((2, 15, 0), (45, 194, 229), 1, "blt")
        if not hasattr(curr_spr, "dmg"):
            curr_spr.dmg = 4
        curr_spr.spd = spd
        curr_spr.rect.center = src.rect.center
        curr_spr.curr_ang = i
        curr_spr.update()
        spr_grp.add(curr_spr)


def polygon_brc(spr, src, spr_grp, spd) -> None:
    midleft = src.rect.midleft
    midright = src.rect.midright
    midbottom = src.rect.midbottom
    blt_index = [
        {'ang': rand.choice([-30, -210]),
         'pos': midleft,},
        {'ang': rand.choice([30, 210]),
         'pos': midright},
        {'ang': rand.choice([90, 270]),
         'pos': midbottom}
    ]

    for blt_info in blt_index:
        curr_spr = spr((2, 15, 0), (45, 194, 229), 1, "blt-cros")
        if not hasattr(curr_spr, "dmg"):
            curr_spr.dmg = 4
        curr_spr.spd = spd
        curr_spr.rect.center = blt_info['pos']
        curr_spr.curr_ang = blt_info['ang']
        curr_spr.update()
        spr_grp.add(curr_spr)


def line_brc(spr, src, spr_grp, _) -> None:
    for _ in range(12):
        curr_spr = spr((2, rand.randint(30, 180), 0), (45, 194, 229), 1, "blt")
        if not hasattr(curr_spr, "dmg"):
            curr_spr.dmg = 6
        curr_spr.spd = 0
        curr_spr.rect.center = src.rect.center
        rands = rand.randint(0, 360)
        curr_spr.curr_ang = rands
        curr_spr.update()
        spr_grp.add(curr_spr)