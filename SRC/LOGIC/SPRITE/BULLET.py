import random as rand

from FRIEND import RectRaining
from FUNC import Spawn
from FUNC import BaseShape


class BulletMgr:
    def __init__(th, proc):
        th.proc = proc

        th.bomb = RectRaining(th.proc)
        th.spr = BaseShape

    def spwn_blt(th):
        p = 2 ** (th.proc("get", "pln", "spt") // 32)
        q = 2 ** (th.proc("get", "pln", "spt") // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                th.bomb.fire(0 + i * 10, 0 + i * 12,
                             j)

        char = th.proc("get", "pln", "char")
        rands = rand.randint(0, 45)
        for i in range(0 + rands, 360 + rands, 45):
            Spawn.spwn_spr(th.spr, None,
                           th.proc("get", "main", "ptcl_grp"),
                           char.rect.center, (6, 10), 0, i,
                           (2, 2), 0, char.clr, 1)

    def single_bomb(th):
        if (not th.proc("get", "pln", "is_sdivide") and
            th.proc("get", "pln", "spt") >= 8):
            th.proc("add", "pln", "spt",
                    -8)
            th.proc("sw", "pln", "is_sdivide",
                    True)

    def use_bomb(th):
        if th.proc("get", "pln", "is_sdivide"):
            th.bomb.free()

    def blt_coll(th, src, tar):
        tar.hp -= src.dmg
        th.proc("add", "pln", "sc",
                64)

        if tar.hp <= 0:
            tar_pos = (tar.rect.centerx, tar.rect.centery)

            if hasattr(tar, "bomb"):
                th.proc("func", "stg", "shhm_lose")()

            rands = rand.randint(0, 45)
            for i in range(0 + rands, 360 + rands, 45):
                Spawn.spwn_spr(th.spr, None,
                               th.proc("get", "main", "ptcl_grp"),
                               tar_pos, (6, 10), 0, i,
                               (2, 2), 0, tar.clr, 1)
            
            th.proc("func", "item", "item_spwn")(tar_pos)
            th.proc("func", "wbrc", "brc_death")(tar, tar_pos)
            
            tar.kill()

        src.kill()