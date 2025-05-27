print("START MINCORE!")
from core.mini import nanogui
import time

pg = nanogui.pg

screen = None

def init(screenA):
    global screen
    screen = screenA

def bsodcall(text: str):
    nanogui.bsod(nanogui.drobic(text, 128), screen)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        time.sleep(0.1)