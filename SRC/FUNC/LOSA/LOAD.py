import random as rand
import json

from ..LOGIC import TOOL


def ld_stg(stg, t_clr, t_bd, pos, wh, hp, spr, spr_grp):
    file = f"AST/STG_{stg[0]}-{stg[1]}.stg"
    row = 0

    for line in TOOL.op_file(False, file).splitlines():
        for i in range(len(line)):
            if line[i] != 'o':
                type = int(line[i])
                bd = rand.choice([t_bd[0]] * t_bd[3] + [t_bd[1], t_bd[2]])
                x = pos[0] + i * wh[0]
                y = pos[1] + row * wh[1]
                clr = t_clr[0] if rand.random() >= t_clr[2] else t_clr[1]

                brc = spr(wh, bd,
                          clr, type,
                          pos=((x, y), (x + wh[0], y)))

                if not hasattr(brc, "hp"):
                    brc.hp = hp
                brc.rect.center = (x, y)

                spr_grp.add(brc)

        row += 1


def ld_txt(stg):
    file = f"AST/TALK_{stg}.json"

    return json.loads(TOOL.op_file(False, file))