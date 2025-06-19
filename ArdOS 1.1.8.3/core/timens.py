print("[Timer]: time")
import time

class Timer:
    """Таймер отсчёта времени"""
    def __init__(self, new: float):
        self.tm = time.time()
        self.new = new
    
    def __call__(self):
        if self.tm + self.new <= time.time():
            return True
        return False