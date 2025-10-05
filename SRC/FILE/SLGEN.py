import random as rand
import json

import BRICK


class SLGen:
    def __init__(th, own):
        th.own = own

        th.row = 0

    def ld_stg(th):
        th.row = 0
        file = f'AST/STG_{th.own.stg_mgr.stg}-{th.own.stg_mgr.lv}.stg'

        for line in th.own.op_file(False,
                                   file).splitlines():
            for i in range(len(line)):
                if line[i] != 'o':
                    brc_type = int(line[i])

                    bd = rand.choice([2] * (30 - th.own.stg_mgr.stg) + [4, 6])

                    brc = BRICK.BaseShape(15, 15, bd,
                                          th.own.clr_dict[th.own.stg_mgr.stg], brc_type)

                    if not hasattr(brc, "hp"):
                        brc.hp = 4 * brc.bd / 2
                    brc.rect.center = (127 + i * 15, 22 + th.row * 15)

                    th.own.brc_grp.add(brc)

            th.row += 1

    def ld_txt(th):
        file = f"AST/TALK_{th.own.stg_mgr.stg}.json"

        return json.loads(th.own.op_file(False,
                                         file))