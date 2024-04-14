import sys
import os

count = 0

def precompile(filepath: str):
    global count
    ++count

    with open(filepath, 'r') as f:
        source = f.read()
    source = compile(source, filepath, 'exec')
    with open(filepath, 'w') as f:
        f.write(source)

def traverse(root: str):
    for entry in os.listdir(root):
        entrypath = os.path.join(root, entry)
        if os.path.isdir(entrypath):
            traverse(entrypath)
        elif entrypath.endswith(".py"):
            precompile(entrypath)

traverse(sys.argv[2])
print(f'预编译成功，一共处理了{count}个文件')
