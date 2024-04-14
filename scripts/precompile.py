import sys
import os

def precompile(filepath: str):
    print('> ' + filepath)
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

