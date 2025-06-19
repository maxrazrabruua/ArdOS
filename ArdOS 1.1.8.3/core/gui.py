print("[GUI]: pygame")
import pygame as pg
print("[GUI]: click")
from core import click
print("[GUI]: Timer")
from core.timens import Timer
print("[GUI]: Ins")
from core.oi import Ins
print("[GUI]: System")
from core.ardos import System
print("[GUI]: zipLib")
from core import zipLib as zipl
print("[GUI]: time")
import time
print("[GUI]: os")
import os
print("[GUI]: keyboard")
import keyboard

pg.init()
pg.mixer.init()

screen = None
system = None
v = {}

def init(new, x: System):
    global screen
    global system
    screen = new
    system = x

def append(newvar: str, value: object):
    global v
    v[newvar] = value

class Overlays:
    def __init__(self, xy: tuple[int, int], wh: tuple[int, int], image: str, update: bool = True):
        self.x, self.y = xy
        self.width, self.heigth = wh
        self.image = pg.image.load(image).convert_alpha()
        self.image = pg.transform.scale(self.image, wh)
        self.update = update
        self.addargs = []
        self._meta = {}
    
    def __call__(self):
        # print(self.addargs)

        screen.blit(self.image, (self.x, self.y))
        if len(self.addargs) != 0:
            pg.draw.rect(screen, self.addargs[0], (self.x, self.y, self.width, self.heigth), self.addargs[1])
        if self.update: pg.display.flip()

class Text:
    def __init__(self, xy: tuple[int, int], width: int, text: str, color: tuple[int, int, int], pixel: bool = False):
        self.text = text
        self.width = width
        self.x, self.y = xy
        self.color = color
        self.pixel = pixel

    def __call__(self):
        font = pg.font.SysFont(None, self.width)
        text_surf = font.render(self.text, not self.pixel, self.color)
        screen.blit(text_surf, (self.x, self.y))

class Style:
    def __init__(self, contour: tuple[int, int, int], color: tuple[int, int, int], upmenu: tuple[int, int, int], color_title: tuple[int, int, int]):
        self.contour = contour
        self.color = color
        self.upmenu = upmenu
        self.color_title = color_title

class Button:
    def __init__(self, image: str, xy: tuple[int, int], wh: tuple[int, int], scripts: tuple[str, str, str]):
        self.image = image
        self.xy = xy
        self.wh = wh
        self.init, self.main, self.click = scripts
        self.cash = {}
        self.local = {}
        self.activity = False
        self.add = {}
        self.initIs = True
    
    def __call__(self):
        if self.activity:
            if self.image in self.cash:
                self.cash[self.image].x, self.cash[self.image].y = self.xy
                self.cash[self.image]()
            else:
                i = None
                try:
                    i = Overlays(self.xy, self.wh, self.image, False)
                except:
                    i = Overlays(self.xy, self.wh, "core/404image.png", False)
                self.cash[self.image] = i
    
    def inPos(self, pos: tuple[int, int]):
        if self.xy[0] <= pos[0] <= self.xy[0] + self.wh[0]:
            if self.xy[1] <= pos[1] <= self.xy[1] + self.wh[1]:
                return True
        return False
    
    def myclick(self):
        mouse_buttons = pg.mouse.get_pressed()
        if mouse_buttons[0]:
            if self.inPos(pg.mouse.get_pos()):
                if 'meneger' in self.add:
                    if self.add['meneger'].getclick(pg.mouse.get_pos(), False):
                        return
                try:
                    exec(self.click)
                except Exception as e:
                    print(f"{e.__class__.__name__}: {str(e)}")
    
    def go(self):
        if self.initIs:
            try:
                exec(self.init)
                self.initIs = False
            except:
                pass
        
        exec(self.main)

        self.myclick()
    
    def inPosA(self):
        mouse_buttons = pg.mouse.get_pressed()
        if mouse_buttons[0]:
            if self.inPos(pg.mouse.get_pos()):
                return True
        return False

print("[GUI]: wins")
from core import wins

class Window:
    def __init__(self, style: Style, xy: tuple[int, int], wh: tuple[int, int], title: str, script: list[dict] = [], pyscripts: tuple[str, str, str, str] = ("", "", "", ""), id: int = 0):
        self.style = style
        self.xy = xy
        self.wh = wh
        self.title = title
        self.activity = False
        self.id = id
        self.script = script
        self.init = pyscripts[0]
        self.main = pyscripts[1]
        self.i = False
        self.local = {}
        self.content = self.script
        self.cash = {
            'images': {},
            'buttons': {}
        }
        self.focus = False
        self.focusScript = pyscripts[2]
        self.add = {}
        self.exit = pyscripts[3]
        self.movable = True
    
    def __call__(self):
        if self.activity:
            self.go(True)
    
    def move(self, mouse: tuple[int, int], save: bool = True):
        if not self.inButton():
            if self.movable:
                if self.activity:
                    # print("b")
                    if not self.inPos(mouse):
                        if save:
                            return
                    # print("a")
                    self.xy = mouse

    def inPos(self, pos: tuple[int, int]):
        if self.activity:
            # print(pos)
            # print(f"{self.xy[0]} <= {pos[0]} <= {self.wh[0] + self.xy[0]}")
            # print(f"{self.xy[1]} <= {pos[1]} <= {self.wh[1] + self.xy[1]}")
            if self.xy[0] <= pos[0] <= self.wh[0] + self.xy[0]:
                # print("d")
                if self.xy[1] - 24 <= pos[1] <= self.wh[1] + self.xy[1]:
                    # print("c")
                    return True
        return False
    
    def buttonClose(self, pos: tuple[int, int]):
        if self.activity:
            if self.xy[0] + self.wh[0] - 24 <= pos[0] <= self.wh[0] + self.xy[0]:
                # print("d1")
                if self.xy[1] - 24 <= pos[1] <= self.wh[1] + self.xy[1]:
                    # print("c1")
                    return True
        return False
    
    def go(self, update: bool | str = False):
        if not update is True:
            pycode = "not run"
            try:
                if not self.activity:
                    if not self.i:
                        pycode = "init"
                        exec(self.init)
                        self.i = True
                pycode = "main"
                exec(self.main)
                if self.focus:
                    pycode = "focus"
                    exec(self.focusScript)
            except Exception as e:
                self.main = "self()"
                self.init = "self()"
                self.script = [
                    {
                        "command": "text",
                        "args": [
                            (0, 0),
                            24,
                            f"error in '{pycode}' oblast running: {e.__class__.__name__}: {str(e)}",
                            (255, 0, 0)
                        ]
                    }
                ]
                self.wh = (10 + (24 * len(f"error in '{pycode}' oblast running: {e.__class__.__name__}: {str(e)}") // 3), 100)
                self()
                print(f"error in '{pycode}' oblast running: {e.__class__.__name__}: {str(e)}")
        elif update is True:
            close = Overlays((self.xy[0] + self.wh[0] - 24, self.xy[1] - 24), (24, 24), "core/close.png", False)
            title = Text((self.xy[0] + 16, self.xy[1] - 20), 24, self.title, self.style.color_title)
            pg.draw.rect(screen, self.style.color, (self.xy[0], self.xy[1], self.wh[0], self.wh[1]))
            pg.draw.rect(screen, self.style.upmenu, (self.xy[0], self.xy[1] - 24, self.wh[0], 24))
            pg.draw.rect(screen, self.style.contour, (self.xy[0], self.xy[1] - 24, self.wh[0], self.wh[1] + 24), 3)
            title()
            close()
            y = 0
            for command in self.script:
                if command["command"] == "text":
                    xy = command["args"][0]
                    width = command["args"][1]
                    text = command["args"][2]
                    try:
                        color = command["args"][3]
                    except:
                        color = (255 - self.style.color[0], 255 - self.style.color[1], 255 - self.style.color[2])
                    if "args2" in command.keys():
                        args2 = command["args2"]
                    try:
                        a = (10 if args2[0] else 0)
                    except:
                        a = 10
                    Text((xy[0] + self.xy[0] + a, xy[1] + self.xy[1] + y), width, text, color)()
                    y += 3 + width + xy[1]
                elif command["command"] == "image":
                    xy = command["args"][0]
                    wh = command["args"][1]
                    text = command["args"][2]
                    try:
                        ots = command["args"][3]
                    except:
                        ots = True
                    if "args2" in command.keys():
                        counter = command["args2"]

                    if not text in self.cash['images'].keys():
                        try:
                            ov = Overlays((xy[0] + self.xy[0] + (10 if ots else 0), xy[1] + self.xy[1] + y), wh, text, False)
                            try:
                                ov.addargs = counter
                            except: pass
                            ov._meta['addy'] = (10 if ots else 0)
                        except:
                            ov = Overlays((xy[0] + self.xy[0] + (10 if ots else 0), xy[1] + self.xy[1] + y), wh, "core/404image.png", False)
                            try:
                                ov.addargs = counter
                            except: pass
                            ov._meta['addy'] = (10 if ots else 0)
                    else:
                        ov = self.cash['images'][text]
                    y += 10 + xy[1] + wh[1]
                    if not text in self.cash['images'].keys():
                        self.cash['images'][text] = ov
                    ov.x = xy[0] + self.xy[0] + (10 if ots else 0)
                    ov.y = xy[1] + self.xy[1] + ov._meta['addy']
                    ov()
                elif command['command'] == 'button':
                    xy = command["args"][0]
                    wh = command["args"][1]
                    text = command["args"][2]
                    name = command["args"][3]
                    scripts = command["args"][4]
                    if name in self.cash['buttons'].keys():
                        button = self.cash['buttons'][name]
                        button.xy = (button.add['xy'][0] + self.xy[0], button.add['xy'][1] + self.xy[1])
                    else:
                        try:
                            button = Button(text, (xy[0] + 10 + self.xy[0], xy[1] + y + self.xy[1]), wh, scripts)
                        except:
                            button = Button("core/404image.png", (xy[0] + 10 + self.xy[0], xy[1] + y + self.xy[1]), wh, scripts)
                        button.add['window'] = self
                        button.add['xy'] = (xy[0] + 10, xy[1] + y)
                        self.cash['buttons'][name] = button
                    self.cash['buttons'][name].go()
                    y += 10 + self.cash['buttons'][name].xy[1]
        else:
            exec(self.exit)
    
    def inButton(self):
        inB = False
        for button in self.cash['buttons'].values():
            if button.inPosA():
                inB = True
        return inB

class WindowMeneger:
    "Менеджер окон"
    def __init__(self):
        self.windows = {}
        self.cash = None
        self.buttons = []
        self.last = False
        self.timerCheck = Timer(1/30)
    
    def __setitem__(self, index: int, window: Window):
        self.windows[index] = window
    
    def __getitem__(self, index: int) -> Window:
        return self.windows[index]

    def __delitem__(self, index: int):
        del self.windows[index]
    
    def append(self, window: Window, sudo: bool = False):
        if (not self.last) or sudo:
            i = self.more() + 1
            window.id = i
            window.add['meneger'] = self
            self.windows[i] = window
        
        if self.timerCheck():
            mouse_buttons = pg.mouse.get_pressed()
            self.last = mouse_buttons[0]
            self.timerCheck = Timer(1/30)
    
    def clear(self):
        self.windows.clear()
    
    def __call__(self, phone: tuple[int, int, int] | None | list = None):
        if self.timerCheck():
            mouse_buttons = pg.mouse.get_pressed()
            self.last = mouse_buttons[0]
            self.timerCheck = Timer(1/30)

        if phone:
            if not isinstance(phone, list):
                screen.fill(phone)
            else:
                image = phone[0]
                if not self.cash:
                    xy = phone[1]
                    try:
                        self.cash = Overlays((0, 0), xy, "files/system/images/wallpapers/" + image, False)
                    except:
                        self.cash = Overlays((0, 0), xy, "files/system/images/wallpapers/404.png", False)
                    self.cash._meta['scr'] = image
                else:
                    if self.cash._meta['scr'] != image:
                        xy = phone[1]
                        self.cash = Overlays((0, 0), xy, image, False)
                        self.cash._meta['scr'] = image
                self.cash()

        for button in self.buttons:
            button.go()

        qq = False
        for window in list(self.windows.values()):
            window.go()
            if window.inButton():
                qq = True
        pg.display.flip()
        return qq
    
    def getclick(self, pos: tuple[int, int], clear: bool = True) -> Window:
        i = -1
        for window in reversed(list(self.windows.values())):
            if window.inPos(pos):
                i = window.id
                break
        if clear: self.clearFocus()
        if i != -1:
            if clear: self.windows[i].focus = True
            return self.windows[i]
    
    def clearFocus(self):
        for window in self.windows.values():
            self.windows[window.id].focus = False
    
    def __len__(self):
        return len(self.windows.keys())
    
    def appendButton(self, button: Button):
        button.add['meneger'] = self
        self.buttons.append(button)
    
    def clear(self):
        self.windows.clear()
    
    def more(self) -> int:
        i = -1
        for window in self.windows.values():
            if window.id > i:
                i = window.id
        return i

class Screenshot:
    def __init__(self):
        pass

    def __call__ (self):
        pg.image.save(screen, "core/files/screen.png")