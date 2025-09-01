class GetScore:
    def __init__(th, own):
        th.own = own

    def get_pow(th):
        return th.own.ttl_s_pt * 128
        
    def no_hurt(th):
        return th.own.no_hurt_cnt * 2048
    
    def pts(th, combo):
        th.own.sc_cnt += 2 ** combo

    def blt_coll(th):
        th.own.sc_cnt += 64