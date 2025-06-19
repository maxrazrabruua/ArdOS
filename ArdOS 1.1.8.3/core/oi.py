class Ins:
    def __init__(self):
        pass

    def write(self, name: str, data: str):
        with open(f"registers/oi/{name}.reg", "w", encoding="utf-8") as file:
            file.write(data)
    
    def read(self, name: str):
        with open(f"registers/oi/{name}.reg", "r", encoding="utf-8") as file:
            content = file.read()
        return content