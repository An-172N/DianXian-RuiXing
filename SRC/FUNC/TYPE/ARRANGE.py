from ..LOGIC import TOOL


def full_menu(sur, fnt, tit="",
              txt1="", txt2="", txt3="",
              ctl1="", ctl2="",
              oth=""):
    txt_type = [
        {"txt": tit, "pos": (128, 25)},
        {"txt": txt1, "pos": (128, 75)},
        {"txt": txt2, "pos": (128, 100)},
        {"txt": txt3, "pos": (128, 125)},
        {"txt": ctl1, "pos": (390, 235)},
        {"txt": ctl2, "pos": (390, 285)},
        {"txt": oth, "pos": (128, 320)}
    ]

    TOOL.draw_rect(sur,
                   345, 330, 0,
                   (120, 15))
    
    for txt_info in txt_type:
        TOOL.txt_func(sur, fnt,
                      txt_info["txt"], txt_info["pos"])

def half_menu(sur, fnt, tit, txt1, txt2):
    txt_type = [
        {"txt": tit, "pos": (125, 268)},
        {"txt": txt1, "pos": (125, 293)},
        {"txt": txt2, "pos": (125, 318)}
    ]

    TOOL.draw_rect(sur,
                   345, 85, 0,
                   (120, 260))
    
    for txt_info in txt_type:
        TOOL.txt_func(sur, fnt,
                      txt_info["txt"], txt_info["pos"])

def situ(sur, fnt, txt1, txt2, txt3, txt4, fps):
    txt_type = [
        {"txt": txt1, "pos": (8, 25)},
        {"txt": txt2, "pos": (8, 270)},
        {"txt": txt3, "pos": (8, 295)},
        {"txt": txt4, "pos": (8, 320)},
        {"txt": fps, "pos": (405, 343)}
    ]

    for txt_info in txt_type:
        TOOL.txt_func(sur, fnt,
                      txt_info["txt"], txt_info["pos"])