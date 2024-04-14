import subprocess
import sys, os

from .config import config

LOG_FILE = 'playground.log'
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

if config.use_playground_console:
    fd = open(LOG_FILE, 'wt', buffering=1, newline='\n', encoding='utf-8')

    sys.stdout = fd
    sys.stderr = fd

    def get_logs():
        with open(LOG_FILE, 'rt', buffering=1, newline='\n', encoding='utf-8', errors='backslashreplace') as f:
            return f.readlines()
else:
    fd = sys.stdout

    def get_logs():
        return ["[控制台未启用]"]


class SeqTask:
    def __init__(self, *tasks):
        self.tasks = tasks
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.tasks):
            raise StopIteration
        task = self.tasks[self.index]
        try:
            ret = next(task)
        except StopIteration:
            self.index += 1

class TaskCommand:
    instance: 'TaskCommand' = None

    def __init__(self, args, cwd=None, shell=False):
        print(' '.join(args))
        self.pipe = subprocess.Popen(args, cwd=cwd, shell=shell, stdout=fd, stderr=fd, encoding='utf-8')
        self.returncode = None
        
    def __iter__(self):
        TaskCommand.instance = self
        return self
    
    def __next__(self):
        if self.pipe is None:
            raise StopIteration
        ret = self.pipe.poll()
        if ret is None:
            return None
        self.returncode = ret
        TaskCommand.instance = None
        raise StopIteration
    
    def kill(self):
        if self.pipe is not None:
            self.pipe.kill()
            self.pipe.wait()
        self.pipe = None
        TaskCommand.instance = None

    def __del__(self):
        self.kill()


def start_vscode(file: str, root: str):
    if sys.platform == "win32":
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Applications\\code.exe\\shell\\open\\command")
        code_path = winreg.QueryValue(key, None)
        if code_path:
            program = code_path.split('"')[1]
            yield from TaskCommand([program, root, file], shell=True)
    elif sys.platform == "darwin":
        yield from TaskCommand(["open", "-a", "Visual Studio Code", root, file])
    else:
        print("功能还未实现")