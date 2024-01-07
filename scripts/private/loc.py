import os

def get_loc(path):
    loc = 0
    with open(path, "rt", encoding='utf-8') as f:
        loc += len(f.readlines())
    return loc

def get_loc_for_dir(path):
    loc = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                _i = get_loc(filepath)
                if _i > 0:
                    print(f"{filepath}: {_i}")
                    loc += _i
    return f'{path}: {loc}'


print(get_loc_for_dir('template/carrotlib'))
print(get_loc_for_dir('projects/magicpd'))
