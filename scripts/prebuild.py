import os, sys
import shutil
from sync_template import sync_template

assert len(sys.argv) == 2, 'Usage: python prebuild.py <project>'
project = sys.argv[1]

sync_template(project)

assets_dir = 'android/app/src/main/assets'

shutil.rmtree(assets_dir, ignore_errors=True)
assert not os.path.exists(assets_dir)
shutil.copytree(project, assets_dir, ignore=shutil.ignore_patterns('*.pyi', '*.ase', '*.aseprite'))
