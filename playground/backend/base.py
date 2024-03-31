import subprocess
import sys

def cmd(args, cwd=None, shell=False):
    print(' '.join(args))
    pipe = subprocess.Popen(args, cwd=cwd, shell=shell)
    pipe.wait()
    assert pipe.returncode == 0, pipe.returncode

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