import zipfile
import os

def unPack(file: str, new: str):
    os.makedirs(new, exist_ok=True)
    with zipfile.ZipFile(file, 'r') as archive:
        archive.extractall(path=new)