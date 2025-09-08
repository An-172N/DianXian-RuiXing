from SDIVIDES.RECTRAINER import RectRainer


class BombManager:
    def __init__(th, own):
        th.own = own
        
        th.rect_rainer = RectRainer(own)

    def single_bomb(th):
        if all([not th.own.pln_mgr.is_use_bomb,
                not th.own.pln_mgr.is_wait_respwn,
                th.own.s_pt >= 16]):
            th.own.s_pt -= 16
            th.own.cooldown_ctr = 0
            th.own.pln_mgr.is_use_bomb = True

    def use_bomb(th):
        if th.own.pln_mgr.is_use_bomb:
            th.rect_rainer.lgc()