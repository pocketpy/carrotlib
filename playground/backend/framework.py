import os
import sys
import shutil

from .base import cmd, TaskCommand

assert sys.platform in ["win32", "linux", "darwin"]

if sys.platform == "win32":
    FRAMEWORK_EXE_PATH = os.path.abspath("build/win32/Release/Game.exe")
else:
    FRAMEWORK_EXE_PATH = os.path.abspath(f"build/{sys.platform}/Game")

FRAMEWORK_BUILD_DIR = os.path.abspath(f"build/{sys.platform}")

def compile_framework():
    if not os.path.exists("3rd/pocketpy/CMakelists.txt"):
        print("初始化子模块")
        task = TaskCommand(["git", "submodule", "update", "--init", "--recursive"])
        yield from task
        if task.returncode != 0:
            return

    shutil.rmtree(FRAMEWORK_BUILD_DIR, ignore_errors=True)
    os.makedirs(FRAMEWORK_BUILD_DIR, exist_ok=True)
    task = TaskCommand(["cmake", "../.."], cwd=FRAMEWORK_BUILD_DIR)
    yield from task
    if task.returncode != 0:
        return
    task = TaskCommand(["cmake", "--build", ".", "--config", "Release"], cwd=FRAMEWORK_BUILD_DIR)
    yield from task
    if task.returncode != 0:
        return
    assert is_framework_compiled()

def is_framework_compiled():
    return os.path.exists(FRAMEWORK_EXE_PATH)
