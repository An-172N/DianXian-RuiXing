class CollideMgr:
    def __init__(th, own):
        th.own = own

    @staticmethod
    def chk_coll(src_grp, tar_grp, coll, src_kill, code):
        for src in src_grp:
            for tar in tar_grp:
                coll_dict = {
                    0: src.rect.colliderect(tar.rect),
                    1: src.rect.collidepoint(tar.rect.center)
                }

                if coll_dict.get(coll):
                    code(src, tar)

                    if src_kill:
                        src.kill()

    def rm_spr(th, spr_grp):
        [spr.kill() for spr in spr_grp
         if not th.own.eff_range.collidepoint(spr.rect.center)]