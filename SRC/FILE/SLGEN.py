import random as rand
import json

import BRICK


class SLGen:
    def __init__(th, proc):
        th.proc = proc

        th.row = 0

    def ld_stg(th):
        th.row = 0
        file = (f"AST/STG_{th.proc('get', 'stg', 'stg')}-"
                f"{th.proc('get', 'stg', 'lv')}.stg")

        for line in th.proc("func", "main", "op")(False,
                                                  file).splitlines():
            for i in range(len(line)):
                if line[i] != 'o':
                    brc_type = int(line[i])

                    bd = rand.choice([2] *
                                     (30 - th.proc("get", "stg", "stg")) + [4, 6])

                    brc = BRICK.BaseShape(15, 15, bd,
                                          th.proc("get", "main", "clr")[th.proc("get", "stg", "stg")], brc_type)

                    if not hasattr(brc, "hp"):
                        brc.hp = 4 * brc.bd / 2
                    brc.rect.center = (127 + i * 15, 22 + th.row * 15)

                    th.proc("get", "main", "brc_grp").add(brc)

            th.row += 1

    def ld_txt(th):
        file = f"AST/TALK_{th.proc('get', 'stg', 'stg')}.json"

        return json.loads(th.proc("func", "main", "op")(False,
                                                        file))