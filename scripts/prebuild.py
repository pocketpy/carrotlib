import os, sys
import shutil
from sync_template import sync_template

assert len(sys.argv) == 2, 'Usage: python prebuild.py <project>'
project = sys.argv[1]

sync_template(project)

# sync assets into the android template project
assets_dir = 'android/app/src/main/assets'
shutil.rmtree(assets_dir, ignore_errors=True)
assert not os.path.exists(assets_dir)
shutil.copytree(project, assets_dir, ignore=shutil.ignore_patterns('*.pyi', '*.ase', '*.aseprite', '*.DS_Store'))

if not os.path.exists('src/tmp'):
    os.mkdir('src/tmp')

def gen_hardcoded_assets(type: str):
    assert type in ['assets', 'sources']
    cpp_file = f'src/tmp/_hardcoded_{type}.cpp'

    with open(cpp_file, 'wt', encoding='utf-8', newline='\n') as f:

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
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                is_source = any(file.endswith(p) for p in SRC_PATTERNS)
                if is_source and type == 'assets':
                    continue
                if not is_source and type == 'sources':
                    continue
                filepath = os.path.relpath(os.path.join(root, file), assets_dir)
                filepath = filepath.replace('\\', '/')
                with open(os.path.join(root, file), 'rb') as const_f:
                    content = const_f.read()
                # print(filepath, len(content) // 1024, 'KB')
                const_array = ','.join([str(b) for b in content])
                f.write(f'    const static unsigned char _{index}[] = {{ {const_array} }};\n')
                f.write(f'    Assets["{filepath}"] = {{ _{index}, {len(content)} }};\n')
                index += 1
        f.write('}\n')

    # print file size of the cpp file
    cpp_file_size = os.path.getsize(cpp_file)
    cpp_file_size = cpp_file_size // 1024
    print(f'Generated {cpp_file} of {index} files of total size {cpp_file_size} KB')

gen_hardcoded_assets('assets')
gen_hardcoded_assets('sources')
