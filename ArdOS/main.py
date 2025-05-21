import pygame as pg
from core import gui
from core.timens import Timer
from core import click
from core.oi import Ins
import time
import keyboard as kb

pg.init()

with open("registers/default/screenX.reg", "r", encoding="utf-8") as file:
    screenX = int(file.read())

with open("registers/default/screenY.reg", "r", encoding="utf-8") as file:
    screenY = int(file.read())

screen = pg.display.set_mode((screenX, screenY))

gui.init(screen)

z = gui.Screenshot()
o = gui.Overlays((300, 150), (200, 172), "logo.png")
t = gui.Text((300, 500), 48, "Start ArdOS...", (255, 255, 255))
m = gui.WindowMeneger()
windows = [gui.Window(gui.Style((127, 127, 127), (255, 255, 255), (0, 0, 255), (255, 255, 255)), (screenX // 3, screenY // 3), (400, 300), "Добро пожаловать в систему!", [
    {
        "command": "image",
        "args": [
            (100, 0),
            (200, 172),
            "whiteLogo.png"
        ],
        "args2": [
            (127, 127, 127),
            5
        ]
    },
    {
        "command": "text",
        "args": [
            (0, 0),
            24,
            "ArdOS 1.0.1"
        ]
    },
    {
        "command": "text",
        "args": [
            (0, 0),
            24,
            "Добро пожаловать!"
        ]
    }
],
(
    "self.activity = True",
    "self()",
    "pass"
))]

t()
o()

al = False
running = True
timer = Timer(3)
s = False
last = (0, 0)
new = None
my = "Hello"
myi = 0
tm = Timer(1)
zr = Timer(1/30)
ach = Timer(1/4)
secT = Timer(1)
fps = 0
with open("registers/default/screenshotStart.reg", "r", encoding="utf-8") as file:
    scr = (True if file.read() == "1" else False)

ins = Ins()
while running:
    if timer() and not al:
        print("ABC")
        screen.fill((0, 255, 0))
        for window in windows:
            m.append(window)
        al = True
    elif al:
        m((0, 255, 0))

    for event in pg.event.get():
        print(m.windows)
        mouse_buttons = pg.mouse.get_pressed()
        if event.type == pg.QUIT:
            with open("registers/default/screenshotStart.reg", "w", encoding="utf-8") as file:
                print(scr)
                file.write("1" if scr else "0")

            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            wm = m.getclick(pg.mouse.get_pos())
            if wm:
                if wm.buttonClose(pg.mouse.get_pos()):
                    print(m.windows, wm.id)
                    del m[wm.id]
                    del wm
                    print("yes!")
                    continue
                print("yes! 1")
            print("yes! 2")

        if mouse_buttons[0] and not s:
            print("0")
            w = m.getclick(pg.mouse.get_pos())
            print(w)
            if w:
                if w.inPos(pg.mouse.get_pos()):
                    s = True
                    w.move(pg.mouse.get_pos(), False)
                    last = pg.mouse.get_pos()
                    new = Timer(1)
        elif mouse_buttons[0] and s:
            print("1")
            w.move(pg.mouse.get_pos(), False)
            last = pg.mouse.get_pos()
            new = Timer(0.1)
        
        if not mouse_buttons[0] and s and new():
            print("2")
            s = False
            w.move(last, False)
        
    if kb.is_pressed("ctrl+t"):
        m.append(gui.Window(gui.Style((64, 64, 64), (0, 0, 0), (127, 127, 127), (255, 255, 255)), (200, 200), (screenX // 2, screenY // 2), "Терминал", [
            {
                "command": "text",
                "args": [
                    (0, 0),
                    24,
                    ""
                ]
            }
        ],
        (
            "\n".join([
                "self.activity = True",
                "self.local['input'] = click.Input()",
                "self.local['timer'] = Timer(0.01)",
                "self.local['index'] = 0"]),
            "\n".join(["self()"]),
            "\n".join([
                "def echo(text, self=self):",
                "   self.content.append({'command': 'text', 'args': [(0, 0), 24, text]})",
                "   self.local['index'] += 1",
                "if self.local['timer']():",
                "   ic = self.local['input']()",
                "   if not ic:",
                "       self.local['timer'] = Timer(0.01)",
                "       self.content[self.local['index']]['args'][2] = self.local['input'].text",
                "   else:",
                "       if self.local['index'] != 6:",
                "           self.content[self.local['index']]['args'][2] = ic",
                "           exec(ic)",
                "           self.local['index'] += 1",
                "           self.content.append({'command': 'text', 'args': [(0, 0), 24, '']})",
                "       else:",
                "           self.local['index'] = 0",
                "           self.content.clear()",
                "           self.content.append({'command': 'text', 'args': [(0, 0), 24, '']})"
            ])
        )))

    # Можно добавить sleep, если ничего не происходит
    fps += 1
    if secT():
        ins.write("fps", str(fps))
        fps = 1
        secT = Timer(1)

    time.sleep(1/60)
    if zr():
        if scr:
            z()
        zr = Timer(1/30)
    
    if ach():
        if kb.is_pressed("ctrl+shift"): # Ивент переключения языка
            click.lang = "ru" if click.lang == "en" else "en"
        elif kb.is_pressed("shift+c"):
            scr = not scr
            print(scr)
        elif kb.is_pressed("ctrl+f"):
            m.append(gui.Window(gui.Style((127, 0, 0), (255, 255, 255), (255, 0, 0), (255, 255, 255)), (100, 100), (200, 60), "FPS-чекер", [
                {
                    "command": "text",
                    "args": [
                        (0, 0),
                        56,
                        "",
                        (255, 0, 0)
                    ]
                }
            ],
            (
                "\n".join([
                    "self.activity = True",
                    "self.local['ins'] = Ins()"
                ]),
                "\n".join([
                    "self.content[0]['args'][2] = self.local['ins'].read('fps')",
                    "self()"
                ]),
                "\n".join([""])
            )))
        arh = Timer(1/4)