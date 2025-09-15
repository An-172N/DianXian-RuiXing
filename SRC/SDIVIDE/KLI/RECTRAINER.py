# from BRICK.BASE.BASESHAPE import BaseShape

# from LOGIC.PROCESS.MOVE import mv


class RectRainer:
    def __init__(th, own):
        th.own = own

    def lgc(th):
        if th.own.fusil_cnt > 0:
            if th.own.fusil_cnt >= 8:
                th.own.is_cnt_fusil = False
                th.own.own.pln_mgr.is_use_sdivide = True

            if not th.own.is_cnt_fusil:
                th.own.spwn_blts()

                th.own.fusil_cnt -= 1
                th.own.own.pln_mgr.s_pt -= 2
            
            if th.own.own.pln_mgr.s_pt < th.own.fusil_cnt * 2 + 1:
                th.own.fusil_cnt = th.own.own.pln_mgr.s_pt // 2

    # def spwn_rect(th):
    #     th.ctr += 1

    #     if (th.ctr >= 60
    #         and th.ctr % 2 == 0
    #         and th.cnt <= 4):
    #         th.cnt += 1

    #         for i in range(120, 466, 15):
    #             blt = BaseShape(15, 15, 0,
    #                             (45, 194, 229), 1, "bomb")

    #             blt.spd = -24
    #             blt.dmg = 6

    #             blt.rect.center = (i, 0)

    #             th.own.blt_grp.add(blt)

    # def upd_rect(th):
    #     for blt in th.own.blt_grp:
    #         if blt.type == "bomb":
    #             mv(blt, blt.spd)

    # def rst_bomb(th):
    #     th.cnt = 0
    #     th.ctr = 0