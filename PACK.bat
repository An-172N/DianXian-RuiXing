nuitka ^
    --standalone ^
    --onefile ^
    --mingw64 ^
    --remove-output ^
    --lto=yes ^
    --windows-console-mode=disable ^
    --enable-plugin=anti-bloat ^
    --file-version="1.0" ^
    --product-version="1.0" ^
    --product-name="RuiXing ~ Thunder Out of the Mountain" ^
    --copyright="Copyright (c) 2025 An_172N" ^
    --windows-icon-from-ico=ASSET\IMAGE\IMG_ICON.png ^
    --include-data-dir=ASSET=ASSET ^
    --output-filename=DX00 ^
    --nofollow-import-to=tkinter,unittest,test,pdb,doctest,setuptools,pip,email,http,urllib,xml,sqlite3,multiprocessing,html,distutils,cgi,cgitb,wsgiref,smtplib,poplib,imaplib,idlelib,pydoc,gettext,locale,threading,ordered_set,venv,ensurepip,ftplib,wave,audioop ^
    --nofollow-import-to=pygame.mixer,pygame.mixer_music,pygame.music,pygame.newbuffer,pygame.pypm,pygame.gfxdraw,pygame.cdrom,pygame.joystick,pygame.mouse,pygame.movie,pygame.overlay,pygame.sndarray,pygame.surfarray,pygame.scrap,pygame.camera,pygame.macosx,pygame.midi,pygame.threads,pygame.examples ^
    --nofollow-import-to=pygame._sdl2,pygame._camera_opencv,pygame._camera_vidcapture,pygame.__pyinstaller,pygame._camera ^
    --nofollow-import-to=numpy ^
    .\MAIN.py