from __future__ import print_function

import json
import os
import os.path
import sys
from xml.dom import Node

import utils
import utils.checks

from forms import Form, BMML

usage = """
define_forms.py - Scans the bmml files for forms and allows the user to enumerate them

Usage: define_forms.py

"""

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

    # Find and build Form objects for all forms found in in bmml files
    bmml_forms = []
    for bmml_file in all_bmmls:
        forms = bmml_file.forms
        if len(forms) != 0:
            bmml_forms.extend(forms)

    choice = 0
    while(choice != 3 and choice != 4):
        print("\nFound %s possible forms within %s bmml files! How do you want to proceed?" % (len(bmml_forms), len(all_bmmls)))
        choice = utils.prompt_choices([
            "Show me the currently configured forms.",
            "Delete a currently configured forms.",
            "Show me auto-detected forms, and ask me what to do with them.",
            "Save + Quit.  We're done here.",
            "Quit.  Throwing away changes.",
            ])
        print()
    
        if choice == 0:
            display_forms(project)
        elif choice == 1:
            delete_a_form(project)
        elif choice == 2:
            ask_autodetected_forms(project, bmml_forms)
        elif choice == 3:
            utils.save_projectjson(project)

def display_forms(project):
    print("%s forms currently configured" % len(project['forms']))
    for form in project['forms']:
        print()
        print(form)

def delete_a_form(project):
    if not project['forms']:
        print("0 forms currently configured\n")
        return
    print("%s forms currently configured" % len(project['forms']))
    print("Delete a form by choosing its number\n")
    choices = []
    for form in project['forms']:
        choices.append(form.name)
    choices[-1] = choices[-1] + '\n'
    choices.append("Don't Delete Anything\n")
    choice = utils.prompt_choices(choices)
    if choice == len(choices) - 1:
        return
    yn = utils.prompt_yn('Really Delete Form "%s"?' % project['forms'][choice].name, False)
    if yn:
        project['forms'].pop(choice)

def ask_autodetected_forms(project, all_forms):
    current_forms = [f.name for f in project['forms']]
    for form in all_forms:
        if form.name in current_forms:
            continue
        print('Group "%s" found in file "%s"' % (form.name, form.bmml.path))
        print(form)
        if utils.prompt_yn("Add this group as a form to the project?"):
            project['forms'].append(form)
            current_forms.append(form.name)

if __name__ == "__main__":
    main()
