print("START MINICORE!")
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
    screen.quit()
    run = True
    print("Вызвана консоль")
    while run:
        try:
            exec(input(">>> "))
        except Exception as e:
            print(f"{e.__class__.__name__}: {str(e)}")
