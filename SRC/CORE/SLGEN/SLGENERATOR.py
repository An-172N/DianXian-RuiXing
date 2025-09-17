import random as rand

from BRICK.BASE.BASESHAPE import BaseShape


class SLGenerator: # 关卡生成器
    def __init__(th, own): # 初始化
        th.own = own

        th.row = 0
        th.cnt = 0

        th.lv_ld = False # 判断是否加载了关卡

    def ld_stg(th):
        # 重置为第0行
        th.row = 0
        # 读取并加载关卡文件
        with open(f'AST/STAGE{th.own.stg_mgr.stg}-{th.own.stg_mgr.lv}.stg') as file:
            for line in file.readlines(): # 遍历文件行数
                col = len(line)

                for i in range(col - 1): # 遍历字符
                    if line[i] != 'o': # 如果字符不是o
                        brc_type = int(line[i]) # 存储砖块类型

                        bd_id = [2, 4, 6, 8] # 砖块厚度
                        clr_dict = { # 砖块颜色字典
                            1: (255, 128, 0), # 第一关（橙色
                            2: (255, 255, 0), # 第二关（黄色
                            3: (0, 255, 0), # 第三关（绿色
                            4: (128, 0, 128), # 第四关（紫色
                            5: (255, 128, 0), # Extra关（橙色
                            6: (255, 255, 255) # 通用（白色
                        }
                        
                        if rand.random() < 0.12 * th.own.stg_mgr.stg + th.own.stg_mgr.lv / 50: # 生成厚砖块概率
                            bd = rand.choice(bd_id)
                        else: # 否则厚度为最薄
                            bd = 2
                        # 否则按照关卡数生成对应砖块
                        clr = clr_dict.get(th.own.stg_mgr.stg)
                        # 创建砖块实例
                        brc = BaseShape(15, 15, bd,
                                        clr, brc_type)
                        # 生命值及其排放
                        brc.hp = 4 * brc.bd / 2
                        brc.rect.center = (127 + i * 15, 22 + th.row * 15)
                        # 加入砖块到砖块精灵组
                        th.own.brc_grp.add(brc)
                # 行数+1
                th.row += 1

        th.lv_ld = True # 加载完毕
        th.own.pln_mgr.no_hurt_cnt += 1 # 先连续无伤+1

    def lgc(th): # 逻辑
        if not th.lv_ld: # 计数生成关卡
            th.cnt += 1

            if th.cnt >= 90: # 计数到90后生成关卡
                th.ld_stg()
        else:
            if len(th.own.brc_grp) == 0:
                th.own.stg_mgr.summ = True # 没有砖块后进入结算画面

            th.cnt = 0

        if (th.own.stg_mgr.lv == 6
            and not th.own.stg_mgr.is_spwn_fri):
            th.own.stg_mgr.spwn_shhm()