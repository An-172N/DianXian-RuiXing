class Invincibility:
    def __init__(th, own):
        th.own = own

    def lgc(th):
        bomb_mgr = th.own.bomb_mgr
        pln_mgr = th.own.pln_mgr

        th.own.cooldown_ctr += 1

        if pln_mgr.is_use_bomb or pln_mgr.coll:
            if th.own.cooldown_ctr >= 256:
                if pln_mgr.is_use_bomb:
                    pln_mgr.is_use_bomb = False
                    bomb_mgr.rect_rainer.rst_bomb()

                pln_mgr.coll = False
                pln_mgr.is_visitable = True
            else:
                pln_mgr.is_visitable = (th.own.cooldown_ctr // 6) % 2 == 0
        else:
            pln_mgr.is_visitable = True