import shutil
import os, io, sys, re

from .project import sync_project_template
from .base import TaskCommand
from .framework import FRAMEWORK_EXE_PATH
from .platform import startfile

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
                with open(os.path.join(root, file), 'rb', encoding='utf-8') as const_f:
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
    shutil.rmtree(ANDROID_ASSETS_DIR, ignore_errors=True)
    assert not os.path.exists(ANDROID_ASSETS_DIR)
    # ignore build/
    shutil.copytree(project, ANDROID_ASSETS_DIR, ignore=shutil.ignore_patterns(
        '*.pyi', '*.ase', '*.aseprite', '*.DS_Store', 'pyrightconfig.json', 'build', '.gitignore',
    ))
    # add everything in template/
    for td in os.listdir('template'):
        src = os.path.join('template', td)
        dst = os.path.join(ANDROID_ASSETS_DIR, td)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    print(f"{project} 预购建成功")

    if hardcode_assets:
        if not os.path.exists('src/tmp'):
            os.mkdir('src/tmp')
        gen_hardcoded_assets('assets')
        gen_hardcoded_assets('sources')
        print(f"{project} 资源数据库构建成功")


def prepare_build_dir(project: str, platform: str):
    build_dir = os.path.join(project, f"build/{platform}/")
    shutil.rmtree(build_dir, ignore_errors=True)
    os.makedirs(build_dir, exist_ok=True)
    return build_dir

def build_android(project: str, open_dir=True):
    prebuild(project, False)
    target_dir = prepare_build_dir(project, 'android')
    if sys.platform == 'win32':
        gradlew_path = os.path.abspath("android\\gradlew.bat")
        task = TaskCommand([gradlew_path, 'build', 'assembleDebug'], cwd="android", shell=True)
        yield from task
        if task.returncode == 0:
            apk_file = 'android/app/build/outputs/apk/debug/app-debug.apk'
            shutil.copy(apk_file, target_dir)
            if open_dir:
                startfile(target_dir)
    else:
        print("功能还未实现")


def build_ios(project: str, open_dir=True):
    prebuild(project, True)
    target_dir = prepare_build_dir(project, 'ios')
    # build Game.xcframework
    task = TaskCommand(['bash', '-e', os.path.join(os.getcwd(), 'build_ios.sh')])
    yield from task
    if task.returncode == 0:
        # copy raylib ios template
        xcode15_dir = os.path.join(target_dir, 'XCode15')
        shutil.copytree('3rd/raylib/projects/XCode15', xcode15_dir)
        shutil.unpack_archive(
            "playground/assets/Frameworks.zip",
            os.path.join(xcode15_dir, 'raylib/Frameworks')
        )
        game_xcframework_path = os.path.join(os.getcwd(), 'build/ios/Game.xcframework')
        raylib_src_path = os.path.abspath(os.path.join(os.getcwd(), "3rd/raylib/src"))
        pbxproj_path = os.path.join(xcode15_dir, 'raylib.xcodeproj/project.pbxproj')
        os.remove(os.path.join(xcode15_dir, 'main.c'))
        # remove main.c and link Game.xcframework
        from pbxproj import XcodeProject
        pbx = XcodeProject.load(os.path.join(xcode15_dir, 'raylib.xcodeproj/project.pbxproj'))
        assert pbx.remove_file_by_id('1BF3FCFC2BAF2CFD00D3B043')
        pbx.add_file(os.path.join(game_xcframework_path, 'ios-arm64/libGame-os64.a'), tree='BUILT_PRODUCTS_DIR')
        pbx.save()
        # alter raylib.xcodeproj
        mapping = {
            '../../../src': raylib_src_path,
            '../../src': raylib_src_path
        }
        with open(pbxproj_path, 'rt', encoding='utf-8') as f:
            pbxproj = f.read()
        for key, value in mapping.items():
            pbxproj = pbxproj.replace(key, value)
        with open(pbxproj_path, 'wt', encoding='utf-8') as f:
            f.write(pbxproj)
        # build app on real device
        script = "xcodebuild -project raylib.xcodeproj -scheme raylib -destination 'generic/platform=iOS' -configuration Debug -sdk iphoneos"
        task = TaskCommand(['bash', '-e', '-c', script], cwd=xcode15_dir)
        yield from task
        if task.returncode == 0 and open_dir:
            startfile(target_dir)


def build_web(project: str, open_dir=True):
    prebuild(project, True)
    target_dir = prepare_build_dir(project, 'web')
    # run build_web.sh
    task = TaskCommand(['bash', '-e', os.path.join(os.getcwd(), 'build_web.sh')])
    yield from task
    if task.returncode == 0:
        shutil.rmtree(target_dir, ignore_errors=True)
        shutil.copytree('build/web', target_dir)
        if open_dir:
            startfile(target_dir)

def build_win32(project: str, open_dir=True):
    prebuild(project, False)
    target_dir = os.path.join(project, "build/win32/")
    shutil.rmtree(target_dir, ignore_errors=True)
    # copy assets
    shutil.copytree(ANDROID_ASSETS_DIR, target_dir)
    # copy Game.exe
    shutil.copy(FRAMEWORK_EXE_PATH, target_dir)
    # open target dir
    if open_dir:
        startfile(target_dir)


def clean_build_dir(project: str):
    dirs = [os.path.join(project, 'build'), 'android/app/build']
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
        print(f"已删除 {d}")