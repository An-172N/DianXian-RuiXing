class Score:
    def __init__(th, own):
        th.own = own

        th.sc_cnt = 0

    def get_pow(th):
        return th.own.pln_mgr.ttl_s_pt * 256
        
    def no_hurt(th):
        return th.own.pln_mgr.no_hurt_cnt * 4096
    
    def pts(th):
        th.sc_cnt += 2 ** th.own.item_mgr.combo

    def blt_coll(th):
        th.sc_cnt += 64