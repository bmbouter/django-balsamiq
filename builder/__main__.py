import sys
from subprocess import Popen, PIPE

from urls import create_urls
from utils import delete_previous_app, create_app

def main():
    check_django_installed()
    delete_previous_app()
    create_app()
    create_urls()

def check_django_installed():
    django_version = Popen(["django-admin.py", "--version"], stdout=PIPE).communicate()[0]
    if '1.3' not in django_version:
        print 'Django %s is installed.  1.3 is required.' % django_version
        sys.exit(1)

main()
