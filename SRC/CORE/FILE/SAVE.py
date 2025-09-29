import json
import os


class Save:
    def __init__(th, own):
        th.own = own

        th.name = ''

    def rd(th):
        folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
        file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{th.name}.json'

        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(file):
            sav = json.loads(th.own.op_file(False,
                                            file))
        else:
            sav = ['锐山抚形日志']

        return sav, file

    def sav(th):
        file = th.rd()

        file[0].append(
            {
                '助记': th.name,
                '分数': th.own.sc_mgr.sc_cnt,
                '最远到达的地方': f"{th.own.stg_mgr.stg} - {th.own.stg_mgr.lv}",
                '记录日期': th.own.datetime(True),
                '拾形点率': th.own.item_mgr.cnt_item_coll()
            }
        )

        str = json.dumps(file[0],
                         indent=4, ensure_ascii=False)
        th.own.op_file(True,
                       file[1],
                       str)