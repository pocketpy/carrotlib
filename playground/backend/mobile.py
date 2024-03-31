import subprocess
import re
import os

from .base import TaskCommand

class MobileDevice:
    def __init__(self, id: str, title: str):
        self.id = id
        self.title = title

class AndroidDevice(MobileDevice):
    pass

class IOSDevice(MobileDevice):
    pass

def get_android_devices() -> list[AndroidDevice]:
    # adb devices -l
    pipe = subprocess.Popen(["adb", "devices", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    stdout, stderr = pipe.communicate()
    if pipe.returncode != 0:
        print(stderr)
        return []
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

def install_apk_and_run(device: AndroidDevice, root: str):
    assert isinstance(device, AndroidDevice)
    apk_path = f"{root}/build/android/app-debug.apk"
    if not os.path.exists(apk_path):
        print(f"{apk_path} 不存在")
        return
    task = TaskCommand(["adb", "-s", device.id, "install", "-r", apk_path])
    yield from task
    if task.returncode != 0:
        return
    task = TaskCommand(["adb", "-s", device.id, "shell", "am", "start", "-n", "game.example.android/.MainActivity"])
    yield from task
    if task.returncode != 0:
        return
    # task = TaskCommand(["adb", "-s", device.id, "logcat", "-s", "CarrotLib:*", "raylib:*"])
    # yield from task
