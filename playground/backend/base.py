import subprocess
import sys, os

LOG_FILE = 'playground.log'
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

fd = open(LOG_FILE, 'wt', buffering=1, newline='\n')

sys.stdout = fd
sys.stderr = fd

def get_logs():
    with open(LOG_FILE, 'rt', buffering=1, newline='\n') as f:
        return f.readlines()

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
    def __init__(self, args, cwd=None, shell=False):
        print(' '.join(args))
        self.pipe = subprocess.Popen(args, cwd=cwd, shell=shell, stdout=fd, stderr=fd)
        self.returncode = None

    def __iter__(self):
        return self
    
    def __next__(self):
        ret = self.pipe.poll()
        if ret is None:
            return None
        self.returncode = ret
        raise StopIteration
    
    def kill(self):
        self.pipe.kill()


def cmd(args, cwd=None, shell=False):
    print(' '.join(args))
    pipe = subprocess.Popen(args, cwd=cwd, shell=shell, stdout=fd, stderr=fd)
    pipe.wait()
    return pipe.returncode

def start_vscode(file: str, root: str):
    if sys.platform == "win32":
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Applications\\code.exe\\shell\\open\\command")
        code_path = winreg.QueryValue(key, None)
        if code_path:
            program = code_path.split('"')[1]
            return TaskCommand([program, root, file], shell=True)
    if sys.platform == "darwin":
        return TaskCommand(["open", "-a", "Visual Studio Code", root, file])
    else:
        print("功能还未实现")