import json
import shutil
import os
import sys
from subprocess import Popen, PIPE

def get_project_json():
    project_file = open('project.json', 'r')
    project_data = ''.join(project_file.readlines())
    return json.loads(project_data)

def delete_previous_app():
    project_json = get_project_json()
    full_app_path = os.path.abspath(project_json['name'])
    if not os.path.isdir(full_app_path):
        return
    user_response = raw_input('\nShould I destroy %s, so I can rebuild it? [n]: ' % full_app_path).lower()
    if user_response != 'y' and user_response != 'yes':
        print '\nI cannot build new project until I delete the old one\n'
        sys.exit(1)
    shutil.rmtree(full_app_path, ignore_errors=True)

def create_app():
    proj_json = get_project_json()
    output = Popen(["django-admin.py", "startapp", proj_json['name']], stdout=PIPE).communicate()[0]
    print output
