def open_directory(title: str, initial_path: str) -> str:
    from tkinter import filedialog
    return filedialog.askdirectory(
        initialdir=initial_path,
        title=title
    )

def get_string() -> str:
    return input("请输入项目名称：")
