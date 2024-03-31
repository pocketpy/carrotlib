import subprocess
import sys
from typing import TYPE_CHECKING

def cmd(args, cwd=None, shell=False) -> bool:
    print(' '.join(args))
    pipe = subprocess.Popen(args, cwd=cwd, shell=shell)
    pipe.wait()
    return pipe.returncode == 0

def start_vscode(file: str, root: str):
    if sys.platform == "win32":
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Applications\\code.exe\\shell\\open\\command")
        code_path = winreg.QueryValue(key, None)
        if code_path:
            program = code_path.split('"')[1]
            cmd([program, root, file], shell=True)
    else:
        raise NotImplementedError