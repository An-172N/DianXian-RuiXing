import random as rand
import math

import FUNC
import SCRIPT.DICT
import SCRIPT.VARIABLE
from SCRIPT.LOGIC.FRIEND import Base
from ..SPRITE import ITEM
from ..PROCESS import STAGE


def spwn_blt():
    if SCRIPT.VARIABLE.can_shoot:
        p = 2 ** (SCRIPT.VARIABLE.spt // 32)
        q = 2 ** (SCRIPT.VARIABLE.spt // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                SCRIPT.VARIABLE.main_char.bomb.fire(
                    0 + i * 10,
                    0 + i * 12,
                    j
                )

        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 45):
            spr = Base((2, 2, 0), SCRIPT.VARIABLE.main_char.clr, 1)
            spr.spd = rand.randint(6, 10)
            spr.rect.center = SCRIPT.VARIABLE.main_char.rect.center
            spr.curr_ang = i
            SCRIPT.VARIABLE.ptcl_grp.add(spr)


def single_bomb():
    if (not SCRIPT.VARIABLE.is_sdivide and
        SCRIPT.VARIABLE.spt >= 16):
        SCRIPT.VARIABLE.spt -= 16
        SCRIPT.VARIABLE.is_sdivide = True


def blt_coll(src, tar):
    if src.type == "blt":
        if getattr(tar, 'is_die', False):
            src.kill()
            return

    tar.hp -= src.dmg
    SCRIPT.VARIABLE.sc += 64

    if tar.hp <= 0:
        tar.is_die = True
        tar_pos = (tar.rect.centerx, tar.rect.centery)

        if hasattr(tar, "bomb"):
            STAGE.shhm_lose()

        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 45):
            spr = Base((2, 2, 0), tar.clr, 1)
            spr.spd = rand.randint(6, 10)
            spr.rect.center = tar_pos
            spr.curr_ang = i
            SCRIPT.VARIABLE.ptcl_grp.add(spr)
            
        ITEM.item_spwn(tar_pos)
        brc_death(tar, tar_pos)
            
        tar.kill()

    if src.type == "blt":
        src.kill()


def brc_death(brc, brc_pos):
    if brc.clr == SCRIPT.DICT.clr_dict[6]:
        proc_dict = {
            0: polygon_brc,
            1: line_brc,
            2: circle_brc
        }

        proc_dict[brc.shape](
            Base,
            brc,
            SCRIPT.VARIABLE.blt_grp,
            16
        )

    difficulty = FUNC.Calculate.fibonacci(
        1,
        2,
        SCRIPT.VARIABLE.stage + 1
    ) / 100
    if rand.random() <= 0.25 + difficulty:
        tupl = rand.choice([(0, 1, 1), (-30, 31, 30)])
        char = SCRIPT.VARIABLE.main_char
        for i in range(tupl[0], tupl[1], tupl[2]):
            spr = Base((9, 9, 0), brc.clr, brc.shape)
            spr.spd = 2
            spr.rect.center = brc_pos
            two_pt = FUNC.Calculate.delta_tuple((char.rect.centerx, char.rect.centery, 0), (spr.rect.centerx, spr.rect.centery, 0))
            spr.curr_ang = math.degrees(math.atan2(-two_pt[0], -two_pt[1])) + i
            SCRIPT.VARIABLE.brg_grp.add(spr)


def circle_brc(spr, src, spr_grp, spd):
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


def polygon_brc(spr, src, spr_grp, spd):
    blt_index = [
        {'ang': rand.choice([-30, -210]),
         'pos': src.rect.midleft,},
        {'ang': rand.choice([30, 210]),
         'pos': src.rect.midright},
        {'ang': rand.choice([90, 270]),
         'pos': src.rect.midbottom}
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


def line_brc(spr, src, spr_grp, _):
    for _ in range(12):
        curr_spr = spr((2, rand.randint(30, 180), 0), (45, 194, 229), 1, "blt")
        if not hasattr(curr_spr, "dmg"):
            curr_spr.dmg = 6
        curr_spr.spd = 0
        curr_spr.rect.center = src.rect.center
        curr_spr.curr_ang = rand.randint(0, 360)
        curr_spr.update()
        spr_grp.add(curr_spr)