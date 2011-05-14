import os

from utils import get_project_json, get_path_inside_app

views_template = """from django.views.generic import TemplateView

"""

def create_views():
    project_json =  get_project_json()
    views_file_path = get_path_inside_app('views.py')
    f = open(views_file_path, 'w')
    f.write(views_template)
    for url in project_json['urls']:
        f.write(build_standard_view(url))
    f.close()

def build_standard_view(url):
    view_string = "def %s(request):\n" % url['name']
    view_string += '    pass\n\n'
    return view_string
