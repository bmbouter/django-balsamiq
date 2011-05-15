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
    def __init__(self, path, json_dict):
        self.path = path
        self.data = json_dict

def main(args):
    project = utils.find_projectjson()

    # This path is relative to the current working directory and to the
    # directory with project.json (since they're the same dir)
    bmml_path = project['bmml_path']

    # Add a "urls" component to the project if not exists
    if "urls" not in project:
        project['urls'] = {}

    # Build a list of all bmml files
    print("Scanning %s for .bmml files" % bmml_path)
    all_bmmls = []
    for dirpath, dirnames, filenames in os.walk(bmml_path):
        for filename in filenames:
            if filename.endswith(".bmml"):
                # Find the path to the bmml relative to the bmml_path. We can
                # do this by stripping off bmml_path from the front of dirpath,
                # but make sure there is no leading slash left on dirpath
                if not dirpath.startswith(bmml_path):
                    raise Exception("Sanity check failed: found a dirpath that did not start with %s. This shouldn't happen, what's going on?" % bmml_path)
                bmml_file = dirpath[len(bmml_path):]
                bmml_file = bmml_file.lstrip("/\\")
                bmml_file = os.path.join(bmml_file, filename)


                # See if there's an existing entry in project['urls'] or if we
                # need to create a new one
                if bmml_file in project['urls']:
                    json_entry = project['urls'][bmml_file]
                    new = False if "name" in json_entry and "regex" in json_entry else True
                else:
                    json_entry = {}
                    project['urls'][bmml_file] = json_entry
                    new = True
                print("\tProcessing %s %s" % (bmml_file,"(NEW!)" if new else ""))

                all_bmmls.append(
                        BMML(
                            bmml_file,
                            json_entry,
                            )
                        )

    print("Found %s bmml files! How do you want to proceed?" % len(all_bmmls))
    main_menu(all_bmmls)

    print()
    print("Saving project.json...")
    utils.save_projectjson(project)

def main_menu(all_bmmls):
    while True:
        choice = utils.prompt_choices([
            "Show me new files one at a time, and ask me what to do with them.",
            "Show me a menu of all the files and let me pick which to edit.",
            "Save + Quit. We're done here."
            ])

        if choice == 0:
            ask_new_files(all_bmmls)
        elif choice == 1:
            choose_files(all_bmmls)
        elif choice == 2:
            return

def ask_new_files(all_bmmls):
    count = 0
    for bmml in all_bmmls:
        if "name" in bmml.data and "regex" in bmml.data:
            # not a "new" file, it already has an entry
            continue
        count += 1
        edit_bmml(bmml)

    print()
    if count == 0:
        print("No new files, all bmml files have an entry already!")
    else:
        print("That's all of them. now what do you want to do?")

def edit_bmml(bmml):
    print()
    print("Regarding \"%s\"" % bmml.path)
    print(utils.split_lines("What should its name be? This is the name"
            " used to reference back-links,"
            " so it should be an identifier"))
    name = utils.prompt_user("Enter name", checks=[utils.checks.identifier]) 

    print()
    print(utils.split_lines("Now, under what URL path should serve this"
            " page? This goes straight to Django's urls file so this"
            " should be a regex"))
    regex = utils.prompt_user("Enter URL regex", checks=[utils.checks.not_empty])

    bmml.data['name'] = name
    bmml.data['regex'] = regex
    print(utils.split_lines("So file %s is going to serve on \"%s\" and have reference name %s" % (bmml.path, regex, name)))
    print("Got it, moving on...")

def choose_files(all_bmmls):
    # Build the menu
    options = []
    for b in all_bmmls:
        options.append(
                "%s\n%s\tr'%s'" % (
                    b.path, 
                    b.data['name'] if 'name' in b.data else "(needs a name)",
                    b.data['regex'] if 'regex' in b.data else "(needs a url)",
                    )
                )

    print()
    print("Choose which BMML file you want to edit")
    choice = utils.prompt_choices(options)
    edit_bmml(all_bmmls[choice])

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
