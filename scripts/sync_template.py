import os
import argparse
import shutil
import json

project_pyright_config = {
    "stubPath": os.path.abspath("template/typings"),
    "extraPaths": [os.path.abspath("template"), os.path.abspath("3rd/pocketpy/include/typings")],
    "reportMissingModuleSource": "none",
    "pythonVersion": "3.10"
}

def sync_template(project: str):
    print(f'sync template for: {project}')
    for td in ['carrotlib']:
        path = os.path.join(project, td)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=False)
        shutil.copytree(os.path.join('template', td), path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--projects', default='projects', required=False, type=str)

    projects = parser.parse_args().projects

    if not os.path.exists(projects):
        print(f'projects path not exists: {projects}')
        exit(1)

    with open(os.path.join(projects, 'pyrightconfig.json'), 'w') as f:
        json.dump(project_pyright_config, f, indent=4)

    for project in os.listdir(projects):
        if '.' in project:
            continue
        sync_template(os.path.join(projects, project))
