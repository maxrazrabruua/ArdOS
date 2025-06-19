print("[ARDOS]: time")
import time

class System:
    def __init__(self):
        self.status = True
        self.screenshoting = False
        self.bootTime = time.time()
        self.realTime = time.time()
    
    def exit(self):
        self.status = False