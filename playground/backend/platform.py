import os, sys
from tkinter import filedialog, Tk

if sys.platform == 'darwin':
    root = Tk()
    root.withdraw()

def open_directory(title: str, initial_path: str) -> str:
    return filedialog.askdirectory(
        initialdir=initial_path,
        title=title
    )

def startfile(arg):
    if sys.platform == 'win32':
        os.startfile(arg)
    elif sys.platform == 'darwin':
        os.system(f'open {arg}')
