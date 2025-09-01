from SDIVIDES.RECTRAINER import RectRainer


class BombManager:
    def __init__(th, own):
        th.own = own
        
        th.rect_rainer = RectRainer(own)

    def single_bomb(th):
        pln_mgr = th.own.pln_mgr

        if all([not pln_mgr.is_use_bomb,
                not pln_mgr.is_wait_respwn,
                th.own.s_pt >= 16]):
            th.own.s_pt -= 16
            th.own.cooldown_ctr = 0
            pln_mgr.is_use_bomb = True

    def use_bomb(th):
        if th.own.pln_mgr.is_use_bomb:
            th.rect_rainer.lgc()