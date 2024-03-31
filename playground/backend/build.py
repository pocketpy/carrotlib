import shutil
import os, io, sys

from .project import sync_project_template
from .base import cmd, TaskCommand
from .framework import FRAMEWORK_EXE_PATH

ANDROID_ASSETS_DIR = 'android/app/src/main/assets'

def gen_hardcoded_assets(type: str):
    assert type in ['assets', 'sources']
    cpp_file = f'src/tmp/_hardcoded_{type}.cpp'
    with io.StringIO(newline='\n') as f:
        f.write(f'''
    #include <map>
    #include <string_view>

    void init_hardcoded_{type}(std::map<
        std::string_view,
        std::pair<const unsigned char*, int>,
        std::less<>
    >& Assets) {{
''')
        SRC_PATTERNS = ['.py', '.pyi', '.json', '.txt', '.csv']
        index = 0
        for root, dirs, files in os.walk(ANDROID_ASSETS_DIR):
            for file in files:
                is_source = any(file.endswith(p) for p in SRC_PATTERNS)
                if is_source and type == 'assets':
                    continue
                if not is_source and type == 'sources':
                    continue
                filepath = os.path.relpath(os.path.join(root, file), ANDROID_ASSETS_DIR)
                filepath = filepath.replace('\\', '/')
                with open(os.path.join(root, file), 'rb') as const_f:
                    content = const_f.read()
                # print(filepath, len(content) // 1024, 'KB')
                const_array = ','.join([str(b) for b in content])
                f.write(f'    const static unsigned char _{index}[] = {{ {const_array} }};\n')
                f.write(f'    Assets["{filepath}"] = {{ _{index}, {len(content)} }};\n')
                index += 1
        f.write('}\n')
        content = f.getvalue()

    if os.path.exists(cpp_file):
        with open(cpp_file, 'rt', encoding='utf-8') as f:
            old_content = f.read()
    else:
        old_content = None
    if old_content != content:
        with open(cpp_file, 'wt', encoding='utf-8') as f:
            f.write(content)
        # print file size of the cpp file
        cpp_file_size = os.path.getsize(cpp_file)
        cpp_file_size = cpp_file_size // 1024
        print(f'Generated {cpp_file} of {index} files of total size {cpp_file_size} KB')
    else:
        print(f'{cpp_file} is up-to-date')


def prebuild(project: str, hardcode_assets: bool):
    sync_project_template(project)
    # sync assets into the android template project
    shutil.rmtree(ANDROID_ASSETS_DIR, ignore_errors=True)
    assert not os.path.exists(ANDROID_ASSETS_DIR)
    # ignore build/
    shutil.copytree(project, ANDROID_ASSETS_DIR, ignore=shutil.ignore_patterns(
        '*.pyi', '*.ase', '*.aseprite', '*.DS_Store', 'pyrightconfig.json', 'build', '.gitignore',
    ))
    print(f"{project} 预购建成功")

    if hardcode_assets:
        if not os.path.exists('src/tmp'):
            os.mkdir('src/tmp')
        gen_hardcoded_assets('assets')
        gen_hardcoded_assets('sources')
        print(f"{project} 资源数据库构建成功")


def build_android(project: str):
    prebuild(project, False)
    target_dir = os.path.join(project, "build/android/")
    shutil.rmtree(target_dir, ignore_errors=True)
    os.makedirs(target_dir, exist_ok=True)
    if sys.platform == 'win32':
        task = TaskCommand([os.path.abspath("android\\gradlew.bat")], cwd="android", shell=True)
        yield from task
        if task.returncode == 0:
            shutil.copy(os.path.join('android/app/build/outputs/apk/debug/app-debug.apk'), target_dir)
            os.startfile(target_dir)
    else:
        print("功能还未实现")


def build_win32(project: str):
    prebuild(project, False)
    target_dir = os.path.join(project, "build/win32/")
    shutil.rmtree(target_dir, ignore_errors=True)
    # copy assets
    shutil.copytree(ANDROID_ASSETS_DIR, target_dir)
    # copy Game.exe
    shutil.copy(FRAMEWORK_EXE_PATH, target_dir)
    # open target dir
    if sys.platform == 'win32':
        os.startfile(target_dir)
        

def build_ios(project: str):
    prebuild(project, True)