class Invincibility:
    def __init__(th, own):
        th.own = own

        th.cd_ctr = 0

    def lgc(th):
        if (th.own.pln_mgr.is_use_sdivide or
            th.own.pln_mgr.coll):
            th.cd_ctr += 1

            if th.cd_ctr >= 256:
                if th.own.pln_mgr.is_use_sdivide:
                    th.own.pln_mgr.is_use_sdivide = False
                    th.own.blt_mgr.rect_rain.rst_bomb()

                th.own.pln_mgr.coll = False
                th.own.pln_mgr.is_visitable = True
            else:
                th.own.pln_mgr.is_visitable = (th.cd_ctr // 6) % 2 == 0
        else:
            th.own.pln_mgr.is_visitable = True