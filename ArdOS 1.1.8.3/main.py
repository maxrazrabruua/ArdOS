try:
    print("[MAIN]: pygame")
    import pygame as pg
    print("[MAIN]: minicore")
    from core.mini import minicore as mini
    try:
        pg.init()
        start = pg.mixer.Sound("files/system/sounds/start.ogg")
        offing = pg.mixer.Sound("files/system/sounds/offing.ogg")
        cl = pg.mixer.Sound("files/system/sounds/click.ogg")
        rw = pg.mixer.Sound("files/system/sounds/responseWindow.ogg")
        rwf = pg.mixer.Sound("files/system/sounds/responseWindowFocus.ogg")
        cl.set_volume(0.33)

        with open("registers/default/screenX.reg", "r", encoding="utf-8") as file:
            screenX = int(file.read())

        with open("registers/default/screenY.reg", "r", encoding="utf-8") as file:
            screenY = int(file.read())

        from core.ardos import System
        screen = pg.display.set_mode((screenX, screenY))
        system = System()

        mini.init(screen)

        print("[MAIN]: gui")
        from core import gui
        print("[MAIN]: Timer")
        from core.timens import Timer
        print("[MAIN]: click")
        from core import click
        print("[MAIN]: Ins")
        from core.oi import Ins
        print("[MAIN]: desktoping")
        from core import desktoping as desktop
        print("[MAIN]: time")
        import time
        print("[MAIN]: keyboard")
        import keyboard as kb

        gui.init(screen, system)

        print("[MAIN]: wins")
        from core import wins

        z = gui.Screenshot()
        o = gui.Overlays((300, 150), (245, 245), "files/system/images/logo.png")
        t = gui.Text((300, 400), 48, "Start ArdOS...", (255, 255, 255))
        m = gui.WindowMeneger()
        desktop.read(m)

        t()
        o()

        al = False
        running = True
        timer = Timer(0)
        s = False
        last = (0, 0)
        new = None
        my = "Hello"
        myi = 0
        tm = Timer(1)
        zr = Timer(1/30)
        ach = Timer(2)
        secT = Timer(1)
        fps = 0
        rclick = True
        with open("registers/default/screenshotStart.reg", "r", encoding="utf-8") as file:
            system.screenshoting = (True if file.read() == "1" else False)

        ins = Ins()
        ttt = False
        qq = Timer(0)
        while running:
            if timer() and not al:
                # print("ABC")
                screen.fill((0, 255, 0))
                wins.go("wellcome", m)
                system.realTime = time.time()
                al = True
                start.play()
            elif al:
                ttt = m([
                    "greenAndBlue.png",
                    (screenX, screenY)
                ])
                if ttt:
                    qq = Timer(3.0)
            for event in pg.event.get():
                # print(m.windows)
                mouse_buttons = pg.mouse.get_pressed()
                if event.type == pg.QUIT or not system.status:
                    with open("registers/default/screenshotStart.reg", "w", encoding="utf-8") as file:
                        # print(system.screenshoting)
                        file.write("1" if system.screenshoting else "0")

                    offing.play()
                    wait = Timer(3)
                    wa = True
                    l = False
                    while wa:
                        if wait():
                            wa = False
                        if al:
                            if not l:
                                wins.go("exit", m, True)
                                l = True

                        for event in pg.event.get():
                            pass
                        m([
                            "greenAndBlue.png",
                            (screenX, screenY)
                        ])
                    running = False

                if qq():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        wm = m.getclick(pg.mouse.get_pos())
                        if wm:
                            if wm.buttonClose(pg.mouse.get_pos()):
                                # print(m.windows, wm.id)
                                wm.go(update="exit")
                                del m[wm.id]
                                del wm
                                # print("yes!")
                                continue
                            # print("yes! 1")
                        # print("yes! 2")

                    if mouse_buttons[0] and not s:
                        # print("0")
                        if rclick:
                            cl.play()
                            rclick = False
                        ww = m.getclick(pg.mouse.get_pos(), False)
                        if ww:
                            if ww.focus:
                                rwf.play()
                            else:
                                rw.play()
                        del ww
                        w = m.getclick(pg.mouse.get_pos())
                        # print(w)
                        if w:
                            if w.inPos(pg.mouse.get_pos()):
                                s = True
                                w.move(pg.mouse.get_pos(), False)
                                last = pg.mouse.get_pos()
                                new = Timer(1)
                    elif mouse_buttons[0] and s:
                        # print("1")
                        w.move(pg.mouse.get_pos(), False)
                        last = pg.mouse.get_pos()
                        new = Timer(0.1)
                    elif not mouse_buttons[0]:
                        rclick = True
                    
                    if not mouse_buttons[0] and s and new():
                        # print("2")
                        s = False
                        w.move(last, False)
                
            if kb.is_pressed("ctrl+t"):
                wins.go("cmd", m)

            # Можно добавить sleep, если ничего не происходит
            fps += 1
            if secT():
                ins.write("fps", str(fps))
                fps = 1
                secT = Timer(1)

            if system.screenshoting: time.sleep(1/60)
            if zr():
                if system.screenshoting:
                    z()
                zr = Timer(1/30)
            
            if ach():
                arh = Timer(2)
                if kb.is_pressed("ctrl+shift"): # Ивент переключения языка
                    click.lang = "ru" if click.lang == "en" else "en"
                elif kb.is_pressed("shift+c"):
                    system.screenshoting = not system.screenshoting
                    # print(system.screenshoting)
                elif kb.is_pressed("ctrl+f"):
                    wins.go("fps-checker", m)
                elif kb.is_pressed("ctrl+r"):
                    wins.go("runner", m)
                    
    except Exception as e:
        mini.bsodcall(f"ERROR: {e.__class__.__name__}: {str(e)}")
except Exception as e:
    run = True
    print(f"ERROR OF ARDOS: {e.__class__.__name__}: {str(e)}")
    print("Привет, ты в меню восстановления\nМы дали тебе доступ к пайтон-консоле чтоб ты свою ArdOS смог восстановить!")
    while run:
        try:
            exec(input(">>> "))
        except Exception as e:
            print(f"{e.__class__.__name__}: {str(e)}")
