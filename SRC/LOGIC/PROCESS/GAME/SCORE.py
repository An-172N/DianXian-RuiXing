class ScoreMgr:
    def __init__(th, own):
        th.own = own

        th.sc_cnt = 0

    def get_pow(th):
        return th.own.pln_mgr.ttl_s_pt * 512
        
    def no_hurt(th):
        return th.own.pln_mgr.no_hurt_cnt * 4096
    
    def pt(th):
        return 2 ** th.own.item_mgr.comb

    def blt_coll(th):
        return 64