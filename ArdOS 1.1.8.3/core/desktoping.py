print("[DESKTOPING]: gui")
from core import gui
print("[DESKTOPING]: ini")
from core import initator as ini
print("[DESKTOPING]: wins")
from core import wins

def read(meneger: "gui.WindowMeneger"):
    with open("files/system/configs/buttons.ini", "r", encoding="utf-8") as file:
        buttons = ini.read(file.read())

    for button in buttons:
        if button != "":
            wins.goButton(button, meneger)