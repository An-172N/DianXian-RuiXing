import json
import os


class Save:
    def __init__(th, own):
        th.own = own

        th.name = ''

    def sav(th):
        folder = f'{os.environ["USERPROFILE"]}/Saved Games/DX00'
        file = f'{os.environ["USERPROFILE"]}/Saved Games/DX00/{th.name}.json'

        if not os.path.exists(folder):
            os.makedirs(folder)

        if os.path.exists(file):
            with open(file, 'r') as f:
                sav = json.load(f)
        else:
            sav = []

        sav.append(
            {
                'name': th.name,
                'score': th.own.sc_mgr.sc_cnt,
                'stg-lv': f"{th.own.stg_mgr.stg} - {th.own.stg_mgr.lv}",
                'time': th.own.date(),
                'coll_per': th.own.item_mgr.cnt_item_coll()
            }
        )

        with open(file, 'w') as f:
            json.dump(sav, f, indent=4)