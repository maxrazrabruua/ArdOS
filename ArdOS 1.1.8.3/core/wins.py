print("[WINS]: gui")
from core import gui

with open("registers/default/error.reg", "r", encoding="utf-8") as file:
    errorS = gui.pg.mixer.Sound(file.read())

def error(title: str, text: str, xy: tuple[int, int], meneger: "gui.WindowMeneger"):
    lenText = 24 * len(text) // 2.5 + 70
    style = gui.Style((127, 0, 0), (255, 255, 255), (255, 0, 0), (255, 255, 255))
    window = gui.Window(style, xy, (lenText, 100), title, [
        {
            "command": "image",
            "args": [
                (0, 15),
                (50, 50),
                "files/system/images/error.png"
            ]
        },
        {
            "command": "text",
            "args": [
                (60, -30),
                24,
                text,
                (255, 0, 0)
            ]
        }
    ],
    (
        "self.activity = True",
        "self()",
        "pass",
        "pass"
    ))
    errorS.play()
    meneger.append(window)

def go(name: str, meneger: "gui.WindowMeneger", sudo: bool = False):
    F = "files/windows/"
    with open(F + name + ".waos", "r", encoding="utf-8") as file:
        data = file.read()
    lines = data.split("\n")
    configs = lines[:3]
    content = "\n".join(lines[3:]).split("**")
    style, info, xywh = tuple(configs)
    xy, wh = tuple(tuple(int(j) for j in i.split(", ")) for i in xywh.split("; "))
    contour, color, upmenu, color_title = tuple([tuple(int(v) for v in c.split(", ")) for c in style.split("; ")])
    meneger.append(gui.Window(gui.Style(contour, color, upmenu, color_title), xy, wh, info, eval(content[0]), (content[1], content[2], content[3], content[4])), sudo)

def goButton(name: str, meneger: "gui.WindowMeneger"):
    F = "files/buttons/"
    with open(F + name + ".baos", "r", encoding="utf-8") as file:
        data = file.read()
    lines = data.split("\n")
    configs = lines[:2]
    content = "\n".join(lines[2:]).split("**")
    info, xywh = tuple(configs)
    xy, wh = tuple(tuple(int(j) for j in i.split(", ")) for i in xywh.split("; "))
    meneger.appendButton(gui.Button(info, xy, wh, (content[0], content[1], content[2])))