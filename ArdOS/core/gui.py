import pygame as pg
from core import click
from core.timens import Timer
from core.oi import Ins
import time
import os
import keyboard

pg.init()

screen = None

def init(new):
    global screen
    screen = new

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

class Window:
    def __init__(self, style: Style, xy: tuple[int, int], wh: tuple[int, int], title: str, script: list[dict] = [], pyscripts: tuple[str, str, str] = ("", "", ""), id: int = 0):
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
            'images': {}
        }
        self.focus = False
        self.focusScript = pyscripts[2]
        self.add = {}
    
    def __call__(self):
        if self.activity:
            self.go(True)
    
    def move(self, mouse: tuple[int, int], save: bool = True):
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
    
    def go(self, update: bool = False):
        if not update:
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
        else:
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


class WindowMeneger:
    "Менеджер окон"
    def __init__(self):
        self.windows = {}
        self.cash = None
    
    def __setitem__(self, index: int, window: Window):
        self.windows[index] = window
    
    def __getitem__(self, index: int) -> Window:
        return self.windows[index]

    def __delitem__(self, index: int):
        del self.windows[index]
    
    def append(self, window: Window):
        window.id = len(self.windows.keys())
        window.add['meneger'] = self
        self.windows[len(self.windows.keys())] = window
    
    def clear(self):
        self.windows.clear()
    
    def __call__(self, phone: tuple[int, int, int] | None | list = None):
        if phone:
            if not isinstance(phone, list):
                screen.fill(phone)
            else:
                image = phone[0]
                if not self.cash:
                    xy = phone[1]
                    try:
                        self.cash = Overlays((0, 0), xy, image, False)
                    except:
                        self.cash = Overlays((0, 0), xy, "files/system/images/wallpapers/404.png", False)
                    self.cash._meta['scr'] = image
                else:
                    if self.cash._meta['scr'] != image:
                        xy = phone[1]
                        self.cash = Overlays((0, 0), xy, image, False)
                        self.cash._meta['scr'] = image
                self.cash()

        for window in list(self.windows.values()):
            window.go()
        pg.display.flip()
    
    def getclick(self, pos: tuple[int, int]) -> Window:
        i = -1
        for window in reversed(list(self.windows.values())):
            if window.inPos(pos):
                i = window.id
                break
        self.clearFocus()
        if i != -1:
            self.windows[i].focus = True
            return self.windows[i]
    
    def clearFocus(self):
        for window in self.windows.values():
            self.windows[window.id].focus = False
    
    def __len__(self):
        return len(self.windows.keys())
    
from core import wins

class Screenshot:
    def __init__(self):
        pass

    def __call__ (self):
        pg.image.save(screen, "core/files/screen.png")