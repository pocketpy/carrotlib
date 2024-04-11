import subprocess
import re, os
from typing import List

from .base import TaskCommand

class MobileDevice:
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title

    def install_and_run(self, root: str):
        raise NotImplementedError


class AndroidDevice(MobileDevice):
    def install_and_run(self, root: str):
        apk_path = f"{root}/build/android/app-debug.apk"
        if not os.path.exists(apk_path):
            print(f"{apk_path} 不存在")
            return
        task = TaskCommand(["adb", "-s", self.id, "install", "-r", apk_path])
        yield from task
        if task.returncode != 0:
            return
        task = TaskCommand(["adb", "-s", self.id, "shell", "am", "start", "-n", "game.example.android/.MainActivity"])
        yield from task
        if task.returncode != 0:
            return
        task = TaskCommand(["adb", "-s", self.id, "logcat", "-s", "CarrotLib:*", "raylib:E"])
        yield from task


class IOSDevice(MobileDevice):
    def install_and_run(self, root: str):
        # brew install ios-deploy
        app_path = f"{root}/build/ios/DerivedData/Build/Products/Debug-iphoneos/raylib.app"
        if not os.path.exists(app_path):
            print(f"{app_path} 不存在")
            return
        task = TaskCommand([
            "ios-deploy",
            "--noninteractive",
            "--unbuffered",
            "--nolldb",
            "--bundle",
            app_path
        ])
        yield from task


def get_android_devices() -> List[AndroidDevice] | None:
    try:
        pipe = subprocess.Popen(["adb", "devices", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, stderr = pipe.communicate()
        if pipe.returncode != 0:
            return None
    except:
        return None
    
    devices = []
    for line in stdout.splitlines():
        if not line or line.startswith("List of devices attached"):
            continue
        id, others = line.split(maxsplit=1)
        # product:OnePlus8T model:KB2005 -> OnePlus8T (KB2005)
        m = re.search(r"product:(\S+) model:(\S+)", others)
        if m:
            title = f"{m.group(1)} ({m.group(2)})"
        else:
            title = "Unknown"
        devices.append(AndroidDevice(id, title))
    return devices

###############################################################
import threading

class ThreadingTask:
    devices: List[MobileDevice]

    def __init__(self):
        self.devices = []
        self.exit_signal = threading.Event()
        self._thread = threading.Thread(target=self._task)
        self._thread.start()

    def _task(self):
        while threading.main_thread().is_alive():
            if self.exit_signal.wait(1):
                break
            devices = get_android_devices()
            if devices is not None:
                self.devices = devices
            else:
                break       # break the loop if adb not found
 
    def dispose(self):
        self.exit_signal.set()
        self._thread.join()

