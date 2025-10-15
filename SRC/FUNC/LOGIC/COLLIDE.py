def chk_coll(src_grp, tar_grp, coll, code):
    for src in src_grp:
        for tar in tar_grp:
            coll_dict = {
                0: src.rect.colliderect(tar.rect),
                1: src.rect.collidepoint(tar.rect.center)
            }

            if coll_dict.get(coll):
                code(src, tar)


def rm_spr(range, spr_grp):
    [spr.kill() for spr in spr_grp
     if not range.collidepoint(spr.rect.center)]