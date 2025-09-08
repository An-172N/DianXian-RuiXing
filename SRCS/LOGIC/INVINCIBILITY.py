class Invincibility:
    def __init__(th, own):
        th.own = own

    def lgc(th):
        th.own.cooldown_ctr += 1

        if th.own.pln_mgr.is_use_bomb or th.own.pln_mgr.coll:
            if th.own.cooldown_ctr >= 256:
                if th.own.pln_mgr.is_use_bomb:
                    th.own.pln_mgr.is_use_bomb = False
                    th.own.bomb_mgr.rect_rainer.rst_bomb()

                th.own.pln_mgr.coll = False
                th.own.pln_mgr.is_visitable = True
            else:
                th.own.pln_mgr.is_visitable = (th.own.cooldown_ctr // 6) % 2 == 0
        else:
            th.own.pln_mgr.is_visitable = True