import subprocess

def cmd(args, cwd=None, **kwargs):
    pipe = subprocess.Popen(args, cwd=cwd, **kwargs)
    pipe.wait()
    assert pipe.returncode == 0, pipe.returncode