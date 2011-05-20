import sys
from subprocess import check_output

from templates import build_template_folders
from urls import create_urls
from utils import delete_previous_app, create_app
from views import create_views

def main():
    check_django_installed()
    delete_previous_app()
    create_app()
    build_template_folders()
    create_urls()
    create_views()

def check_django_installed():
    django_version = check_output(["django-admin.py", "--version"])
    if '1.3' not in django_version:
        print 'Django %s is installed.  1.3 is required.' % django_version
        sys.exit(1)

main()
