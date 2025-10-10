import json
import os


class Save:
    def __init__(th, proc):
        th.proc = proc

        th.name = ''

    def rd(th):
        folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
        file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{th.name}.json'

        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(file):
            sav = json.loads(th.proc('func', 'main', 'op')(False, file))
        else:
            sav = ['锐山抚形日志']

        return sav, file

    def sav(th):
        file = th.rd()

        file[0].append(
            {
                '助记': th.name,
                '分数': th.proc("get", "pln", "sc"),
                '最远到达的地方': (f"{th.proc('get', 'stg', 'stg')} - "
                                  f"{th.proc('get', 'stg', 'lv')}"),
                '记录日期': th.proc('func', 'main', 'dt')(True),
            }
        )

        str = json.dumps(file[0], indent=4)
        th.proc('func', 'main', 'op')(True,
                                      file[1],
                                      str)