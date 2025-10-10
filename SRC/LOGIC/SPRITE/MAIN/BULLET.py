import random as rand

import BRICK


class BulletMgr:
    def __init__(th, proc):
        th.proc = proc

        th.is_fusil = False

        th.fusil_cnt = 0

        th.bomb = BRICK.RectRaining(th.proc)

    def spwn_blt(th):
        p = 2 ** (th.proc("get", "pln", "spt") // 32)
        q = 2 ** (th.proc("get", "pln", "spt") // 16)

        for i in range(0, p):
            for j in range(-q, q + 1, q):
                th.bomb.fire(0 + i * 10, 0 + i * 12,
                             j)
                
        th.proc("func", "ptcl", "ptcl")(th.proc("get", "pln", "char"), 2,
                                        th.proc("get", "pln", "char").clr)

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

    def use_fusil(th):
        if (th.fusil_cnt > 0 and
            not th.is_fusil):
            th.spwn_blt()

            th.fusil_cnt -= 1

    def blt_coll(th, src, tar):
        tar.hp -= src.dmg
        th.proc("add", "pln", "sc",
                64)

        if tar.hp <= 0:
            if hasattr(tar, "bomb"):
                th.proc("func", "stg", "shhm_lose")()
            elif rand.random() <= 0.24:
                th.proc("func", "item", "item")(th.proc("get", "main", "clr")[5], 1,
                                                (tar.rect.centerx, tar.rect.centery))
            elif rand.random() <= 0.001:
                th.proc("func", "item", "item")(th.proc("get", "main", "clr")[3], 2,
                                                (tar.rect.centerx, tar.rect.centery))
            elif rand.random() <= 0.24:
                th.proc("func", "brg", "brg")(tar, rand.choice([(0, 1, 1),
                                                                (-30, 31, 30)]))

            th.proc("func", "ptcl", "ptcl")(tar, 2,
                                            tar.clr, th.proc("get", "main", "clr")[6])
            
            tar.kill()