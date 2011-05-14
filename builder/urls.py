import json
import os
from subprocess import Popen, PIPE

from utils import get_project_json

urls_template = """from django.conf.urls.defaults import *

urlpatterns = patterns('',
"""

def create_urls():
    project_json =  get_project_json()
    urls_file_path = os.path.join(os.path.abspath(project_json['name']), 'urls.py')
    f = open(urls_file_path, 'w')
    f.write(urls_template)
    for url in project_json['urls']:
        url_view = '%s.views.%s' % (project_json['name'], url['name'])
        f.write("    (r'%s', '%s', name='%s')," % (url['path'], url_view, url['name']))
    f.write('\n)\n')
    f.close()
