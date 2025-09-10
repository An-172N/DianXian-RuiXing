from SDIVIDE.KLI.RECTRAINER import RectRainer


class Bomb:
    def __init__(th, own):
        th.own = own
        
        th.rect_rainer = RectRainer(own)

    def single_bomb(th):
        if all([not th.own.pln_mgr.is_use_bomb,
                not th.own.pln_mgr.is_wait_respwn,
                th.own.pln_mgr.s_pt >= 16]):
            th.own.pln_mgr.s_pt -= 16
            th.own.invinc.cd_ctr = 0
            th.own.pln_mgr.is_use_bomb = True

    def use_bomb(th):
        if th.own.pln_mgr.is_use_bomb:
            th.rect_rainer.lgc()