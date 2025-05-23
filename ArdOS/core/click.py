import keyboard as kb
from core.timens import Timer

lang = "en"

def getOfIndex(x: object, y: list, z: list):
    i = -1
    for j, w in zip(y, z):
        i += 1
        if x == w:
            if z[y.index(y[i])] == x:
                print(repr(z[y.index(y[i])]), repr(x))
                return y[i]
    print(repr(x))
    return x

def liter(key: str):
    enkeys = list("`1234567890-=qwertyuiop[]asdfghjkl;'\\zxcvbnm,./ ")
    rukeys = list("ё1234567890-=йцукенгшщзхъфывапролджэ\\ячсмитьбю. ")
    if lang != "en":
        return getOfIndex(key, rukeys, enkeys)
    return key

def upen(key: str):
    dr = list("`1234567890-=qwertyuiop[]asdfghjkl;'\\zxcvbnm,./ ")
    ur = list("~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>? ")
    s = {d: u for d, u in zip(dr, ur)}
    try:
        return s[key]
    except:
        return ""

def downen(key: str):
    dr = list("`1234567890-=qwertyuiop[]asdfghjkl;'\\zxcvbnm,./ ")
    ur = list("~!@#$%^&*()_+QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>? ")
    s = {u: d for d, u in zip(dr, ur)}
    try:
        return s[key]
    except:
        return ""

def upru(key: str):
    dr = list("ё1234567890-=йцукенгшщзхъфывапролджэ\\ячсмитьбю. ")
    ur = list("Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ, ")
    s = {d: u for d, u in zip(dr, ur)}
    try:
        return s[key]
    except:
        return ""

def downru(key: str):
    dr = list("ё1234567890-=йцукенгшщзхъфывапролджэ\\ячсмитьбю. ")
    ur = list("Ё!\"№;%:?*()_+ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ, ")
    s = {u: d for d, u in zip(dr, ur)}
    try:
        return s[key]
    except:
        return ""

class Input:
    class Filter:
        def __init__(self):
            pass

        def ready(self, keys: list[str]):
            l = []
            for key in keys:
                if key == "grave":
                    key = "`"
                if key in list("`1234567890-=qwertyuiop[]asdfghjkl;'\\zxcvbnm,./ "):
                    l.append(key)
                elif key == "space":
                    l.append(" ")
            return l
        
        def main(self, keys: list[str]):
            return str(keys[0] if len(keys) != 0 else "")

    def __init__(self):
        self.text = ""
        self.caps = False
        self.filterclass = self.Filter()
        self.hold = Timer(0.5)
        self.holdedKey = ""
        self.lastKey = ""
    
    def check(self) -> list[str]:
        keys = []
        for key in list("1234567890-=qwertyuiop[]asdfghjkl;'\\zxcvbnm,./") + ["grave", "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12", "insert", "home", "delete", "end", "tab", "caps lock", "shift", "esc", "ctrl", "alt", "backspace", "enter", "space"]:
            if kb.is_pressed(key):
                keys.append(key)
        return keys
    
    def capsed(self):
        self.caps = not self.caps

    def shifted(self, shift: bool):
        return shift if not self.caps else not shift
    
    def __call__(self):
        keys = self.check()
        if "backspace" in keys:
            self.text = self.text[:-1]
        elif "enter" in keys:
            send = self.text[:]
            self.text = ""
            return send
        else:
            k = self.filterclass.ready(keys)
            key = self.filterclass.main(k)
            if (key != self.holdedKey or self.hold()) or (key in ["backspace", "enter"] or key != self.holdedKey):
                if (key != self.holdedKey) or (key != self.lastKey):
                    self.holdedKey = key
                    self.hold = Timer(0.5)
                ka = liter(key)
                shift = "shift" in keys
                if "caps lock" in keys:
                    self.caps = not self.caps
                sh = self.shifted(shift)
                text = ka
                if lang == "ru":
                    if sh:
                        text = upru(text)
                else:
                    if sh:
                        text = upen(text)
                self.text += text
                self.lastKey = key
