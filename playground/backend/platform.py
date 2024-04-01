import os, sys

def open_directory(title: str, initial_path: str) -> str:
    from tkinter import filedialog
    return filedialog.askdirectory(
        initialdir=initial_path,
        title=title
    )

def get_string() -> str:
    return input("请输入项目名称：")

def startfile(arg):
    if sys.platform == 'win32':
        os.startfile(arg)
    elif sys.platform == 'darwin':
        os.system(f'open {arg}')
