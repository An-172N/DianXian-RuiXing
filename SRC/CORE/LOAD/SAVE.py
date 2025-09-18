import json
import os


class Save:
    def __init__(th, own):
        th.own = own

        th.name = ''

        th.is_sav = False

    def sav(th):
        filename = f'SAV/{th.name}.json'

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                sav = json.load(file)
        else:
            sav = []

        sav.append(
            {
                'name': th.name,
                'score': th.own.sc_mgr.sc_cnt,
                'stg-lv': f"{th.own.stg_mgr.stg} - {th.own.stg_mgr.lv}",
                'time': th.own.date(),
                'coll_per': th.cnt_item_coll()
            }
        )

        with open(filename, 'w') as file:
            json.dump(sav, file, indent=4)

    def cnt_item_coll(th):
        return f"{(th.own.item_mgr.coll_item_cnt / th.own.item_mgr.item_cnt) * 100:.2f} %"

    def exit(th):
        th.sav()

        th.own.rst_mgr.rst_game()