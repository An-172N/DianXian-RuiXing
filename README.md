锐行 ~ Thunder Out of the Mountain
=

**这是自己做的一款小游戏**

**在今年（2025）年初开始做的**

**一开始的几个月是想着做STG游戏的** *（没错，我是个东方众*

**然而自己不会设计弹幕** *（数学不会口牙*

**所以在7月份就想着重做成打砖块游戏** *（看着东方灵异传就有了灵感了*

**设定是有3+1关** *（因为懒*

**——**

**说一下玩法吧**

**z是蓄力，松开后会根据蓄力点释放常形力** *（就是发射子弹* 

**x是快移动**

**c是释放形分** *（也就是Bomb*

**在对话中按z看下一则对话，也可以按x跳过**

**白色形点加蓄力，蓝色形点加形力，绿色形点加形闪**

**12点形力可以释放一次形分**

**蓄力上限为6点，不蓄力则照常释放常形力**

**在2.25秒内拾形力点和形闪点可以加combo，最多能combo 16点，拾任何形点可以重新计时，加分规则为2^n**

**如果在结算中保有combo数会额外加combox2分, combo为0的话加1分**

**弹幕生成概率由斐波那契数列计算而成**

**白色砖块会结合附近的砖块类型和攻击形力产生不同的爆破** *（说人话就是每个面的白色砖块有不同的爆炸效果*

**形力就是火力**

**可以存游玩信息，保存目录在用户目录里的“保存的游戏”文件夹**

**——**

**前情提要** *（*

**“差不多深夜了，罗怎么还没回来呢？”**

**“该不会出事了吧？”**

**“不行，我得出去一趟！”**

**说罢，K.璃就出门了**

**“话说……这天气……真的……非常不让人……舒服……”**

**——**

**备注**

**本项目采用GNU GPL-3.0授权**

**项目包含GNU Unifont字体，该字体也在GNU GPL-3.0下使用**

**项目使用的第三方库为Pygame**

**项目使用Nuitka工具进行打包分发，打包指令如下**

```cmd
nuitka ^
    --standalone ^
    --onefile ^
    --mingw64 ^
    --remove-output ^
    --lto=yes ^
    --windows-console-mode=disable ^
    --enable-plugin=anti-bloat ^
    --file-version="1.0.1" ^
    --product-version="1.0.1" ^
    --product-name="RuiXing ~ Thunder Out of the Mountain" ^
    --company-name="An_172N" ^
    --file-description="RuiXing ~ Thunder Out of the Mountain" ^
    --copyright="Copyright (c) 2025, 26 An_172N" ^
    --windows-icon-from-ico=ASSET\IMAGE\IMG_ICON.png ^
    --include-data-dir=ASSET=ASSET ^
    --output-filename=DX00 ^
    --nofollow-import-to=pdb,doctest,unittest,idlelib ^
    --nofollow-import-to=tkinter,email,xml ^
    --nofollow-import-to=ensurepip,venv,distutils ^
    --nofollow-import-to=http,cgi,smtplib,multiprocessing ^
    --nofollow-import-to=numpy,timidity,pygame.examples ^
    .\MAIN.py
```

**项目网址：https://github.com/An-172N/DianXian-RuiXing**

**——An_172N**