from __future__ import print_function

import json
import os
import os.path
import sys
from xml.dom.minidom import parse
from urllib import unquote

import utils
import utils.checks

usage = """
define_forms.py - Scans the bmml files for forms and allows the user to enumerate them

Usage: define_forms.py

"""

class BMML(object):
    def __init__(self, path):
        self.path = path
        import pdb;pdb.set_trace()
        self.dom = parse(path)

    def find_grouped(self):
        groups = []
        for control in self.dom.getElementsByTagName('control'):
            if '__group__' == control.getAttribute('controlTypeID'):
                groups.append(Form(self, control))
        return groups

def dfs_handle_node(node, results):
    for child in node.childNodes:
        dfs_handle_node(child, results)
    if node.nodeType != 1:
        print('     skipping: %s' % node)
    print('visiting: %s' % node)

class Form(object):
    def __init__(self, bmml, dom):
        self.bmml = bmml
        self.dom = dom
        self.name = dom.getElementsByTagName('controlName')[0].childNodes[0].nodeValue
        self.name = unquote(self.name)

    @property
    def elements(self):
        results = []
        return dfs_handle_node(self.dom, results)

    def __unicode__(self):
        import pdb;pdb.set_trace()
        return unicode('okok')

    def __repr__(self):
        return self.__unicode__()

def main():
    project = utils.find_projectjson()

    bmml_path = project['bmml_path']

    # Add a "forms" component to the project if not exists
    if "forms" not in project:
        project['forms'] = []

    # Build a list of all bmml files
    print("Scanning %s for .bmml files" % bmml_path)
    all_bmmls = []
    for dirpath, dirnames, filenames in os.walk(bmml_path):
        for filename in filenames:
            if filename.endswith(".bmml"):
                all_bmmls.append(
                        BMML(
                            os.path.join(dirpath, filename)
                            )
                        )

    # Find all __group__ controls in bmml files
    all_groups = []
    for bmml_file in all_bmmls:
        groups = bmml_file.find_grouped()
        if len(groups) != 0:
            all_groups.extend(groups)

    choice = 0
    while(choice != 4):
        print("\nFound %s possible forms within %s bmml files! How do you want to proceed?" % (len(all_groups), len(all_bmmls)))
        choice = utils.prompt_choices([
            "Show me the currently configured forms.",
            "Edit currently configured forms.",
            "Show me auto-detected forms, and ask me what to do with them.",
            "Let me build a form manually.",
            "Save + Quit.  We're done here.",
            ])
    
        if choice == 0:
            show_current_forms(project)
        elif choice == 1:
            edit_current_forms(project)
        elif choice == 2:
            ask_autodetected_forms(all_groups)
        elif choice == 3:
            choose_files(all_bmmls)

    # Save the forms back to project.json
    f = open('project.json', 'w')
    f.write(json.dumps(project))
    f.close()

def show_current_forms(project):
    print("%s forms currently configured" % len(project['forms']))
    for form in project['forms']:
        choices.append(form.bmml)

def edit_current_forms(project):
    if not project['forms']:
        print("You currently have no forms configured")
        return
    print("%s forms currently configured" % len(project['forms']))
    choices = []
    forms = []
    for form in project['forms']:
        choices.append(form.bmml)
        forms.append(form)
    choice = utils.prompt_choices(choices)

def ask_autodetected_forms(all_grouped):
    for group in all_grouped:
        print()
        print("Regarding Form name='%s'" % group.name)
        print(group.elements)
        regex = utils.prompt_yn("Add this form to the project?")

if __name__ == "__main__":
    main()
