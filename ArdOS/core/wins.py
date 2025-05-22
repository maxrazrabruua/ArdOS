from core import gui

def error(title: str, text: str, xy: tuple[int, int]):
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
        ""
    ))
    return window

def go(name: str, meneger: gui.WindowMeneger):
    F = "files/windows/"
    with open(F + name + ".waos", "r", encoding="utf-8") as file:
        data = file.read()
    lines = data.split("\n")
    configs = lines[:3]
    content = "\n".join(lines[3:]).split("**")
    style, info, xywh = tuple(configs)
    xy, wh = tuple(tuple(int(j) for j in i.split(", ")) for i in xywh.split("; "))
    contour, color, upmenu, color_title = tuple([tuple(int(v) for v in c.split(", ")) for c in style.split("; ")])
    print(repr(xy), repr(wh), repr(info))
    print(content[0])
    print("**")
    print(content[1])
    print("**")
    print(content[2])
    print("**")
    print(content[3])
    print("dict:", eval(content[0]))
    meneger.append(gui.Window(gui.Style(contour, color, upmenu, color_title), xy, wh, info, eval(content[0]), (content[1], content[2], content[3])))