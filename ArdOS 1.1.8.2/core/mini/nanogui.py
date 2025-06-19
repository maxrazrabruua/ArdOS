import pygame as pg


class Text:
    def __init__(self, xy: tuple[int, int], width: int, text: str, color: tuple[int, int, int], pixel: bool = False):
        self.text = text
        self.width = width
        self.x, self.y = xy
        self.color = color
        self.pixel = pixel

    def __call__(self, screen):
        font = pg.font.SysFont(None, self.width)
        text_surf = font.render(self.text, not self.pixel, self.color)
        screen.blit(text_surf, (self.x, self.y))

def drobic(text: str, k: int):
    t = ""
    for i in text:
        if len(t) % k == 0:
            t += "\t"
        t += i
    t = t[1:]
    return t.split("\t")

def bsod(ins: list[str], screen):
    y = 0


    screen.fill((0, 0, 255))
    for string in ins:
        t = Text((0, y + 24), 24, string, (255, 255, 255))
        t(screen)
        y += 24 + 10
    pg.display.flip()