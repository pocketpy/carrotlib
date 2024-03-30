import os
import sys
import shutil

from .base import cmd

assert sys.platform in ["win32", "linux", "darwin"]

if sys.platform == "win32":
    FRAMEWORK_EXE_PATH = "build/win32/Release/Game.exe"
else:
    FRAMEWORK_EXE_PATH = f"build/{sys.platform}/Game"

FRAMEWORK_BUILD_DIR = f"build/{sys.platform}"

def compile_framework():
    shutil.rmtree(FRAMEWORK_BUILD_DIR, ignore_errors=True)
    os.makedirs(FRAMEWORK_BUILD_DIR, exist_ok=True)
    # cmake ../..
    cmd(["cmake", "../.."], cwd=FRAMEWORK_BUILD_DIR)
    # cmake --build . --config Release
    cmd(["cmake", "--build", ".", "--config", "Release"], cwd=FRAMEWORK_BUILD_DIR)
    assert is_framework_compiled()

def is_framework_compiled():
    return os.path.exists(FRAMEWORK_EXE_PATH)
