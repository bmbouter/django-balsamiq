from __future__ import print_function

import json
import os
import os.path
import sys

import utils
import utils.checks

usage = """
gather_urls.py - Scans for bmml files and asks for page names and urls

Usage: start_project.py [project directory]

output directory
    The path that contains your project.json

"""

class BMML(object):
    def __init__(self, path):
        self.path = path

def main(args):
    project = utils.find_projectjson(args[0] if args else None)

    bmml_path = project['bmml_path']
    # XXX deal with relative paths here: relative paths are relative to the
    # project.json file, not to the current directory

    # Add a "urls" component to the project if not exists
    if "urls" not in project:
        project['urls'] = []

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

    print("Found %s bmml files! How do you want to proceed?" % len(all_bmmls))
    choice = utils.prompt_choices([
        "Show me the files one at a time, and ask me what to do with them.",
        "Show me a menu of all the files and let me pick which to edit.",
        ])

    if choice == 0:
        ask_all_files(all_bmmls)
    elif choice == 1:
        choose_files(all_bmmls)

def ask_all_files(all_bmmls):
    for bmml in all_bmmls:
        print()
        print("Regarding %s" % bmml.path)
        print(utils.split_lines(("What should its name be? This is the name"
                " used to reference back-links,"
                " so it should be an identifier"))
        name = utils.prompt_user("Enter name", checks=[utils.checks.identifier]) 

        print(utils.split_lines("Now, under what URL path should serve this"
                " page? This goes straight to Django's urls file so this"
                " should be a regex"))
        regex = utils.prompt_user("Enter URL regex", checks=[utils.checks.not_empty])

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
