import random as rand
import json

from ..LOGIC import TOOL
from ..BRICK.BASESHAPE import BaseShape


def ld_stg(stg, lv, clr1, clr2, pos, wh, hp, bd_per, spr_grp):
    file = f"AST/STG_{stg}-{lv}.stg"
    row = 0

    for line in TOOL.op_file(False, file).splitlines():
        for i in range(len(line)):
            if line[i] != 'o':
                type = int(line[i])
                bd = rand.choice([2] * bd_per + [4, 6])
                x = pos[0] + i * wh[0]
                y = pos[1] + row * wh[1]
                clr = clr1 if rand.random() >= 0.04 else clr2

                brc = BaseShape(wh, bd,
                                clr, type,
                                pos1=(x, y), pos2=(x + 15, y))

                if not hasattr(brc, "hp"):
                    brc.hp = hp
                brc.rect.center = (x, y)

                spr_grp.add(brc)

        row += 1


def ld_txt(stg):
    file = f"AST/TALK_{stg}.json"

    return json.loads(TOOL.op_file(False, file))