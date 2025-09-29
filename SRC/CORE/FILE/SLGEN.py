import random as rand
import json

from BRICK.BASE.TWOBASE import TwoBase


class SLGen:
    def __init__(th, own):
        th.own = own

        th.row = 0
        th.ctr = 0

        th.lv_ld = False

    def ld_stg(th):
        th.row = 0
        file = f'AST/STG_{th.own.stg_mgr.stg}-{th.own.stg_mgr.lv}.stg'

        for line in th.own.op_file(False,
                                   file).splitlines():
            for i in range(len(line)):
                if line[i] != 'o':
                    brc_type = int(line[i])

                    bd_id = [2] * (30 - th.own.stg_mgr.stg) + [4, 6]
                    clr_dict = {
                        1: (255, 128, 0),
                        2: (255, 255, 0),
                        3: (0, 255, 0),
                        4: (128, 0, 128),
                        5: (255, 255, 255)
                    }

                    bd = rand.choice(bd_id)

                    clr = clr_dict.get(th.own.stg_mgr.stg)

                    brc = TwoBase(15, 15, bd, clr, brc_type)

                    brc.hp = 4 * brc.bd / 2
                    brc.rect.center = (127 + i * 15, 22 + th.row * 15)

                    th.own.brc_grp.add(brc)

            th.row += 1

    def ld_txt(th):
        file = f"AST/TALK_{th.own.stg_mgr.stg}.json"

        return json.loads(th.own.op_file(False,
                                         file))

    def sl_proc(th):
        if not th.lv_ld:
            th.ctr += 1

            if th.ctr >= 90:
                th.ld_stg()
                th.lv_ld = True
        else:
            if len(th.own.brc_grp) == 0:
                th.own.stg_mgr.summ = True

            th.ctr = 0