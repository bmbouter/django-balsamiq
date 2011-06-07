from __future__ import print_function

import json
import os
import os.path
import sys

import utils
import utils.checks

usage = """
url_method_types.py - Scans for bmml files and asks for html method types and
return types

Usage: start_project.py

"""

class BMML(object):
    def __init__(self, path, json_dict):
        self.path = path
        self.data = json_dict

    def is_new(self):
        return not ("method_types" in self.data and "return_types" in self.data)

from forms import BMML

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
                else:
                    json_entry = {}
                    project['urls'][bmml_file] = json_entry

                bmml_obj = BMML(
                                bmml_file,
                                json_entry,
                            )
                print("\tProcessing %s %s" % (bmml_file,"(NEW!)" if bmml_obj.is_new() else ""))

                all_bmmls.append(
                            bmml_obj
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
        if not bmml.is_new():
            # not a "new" file, it already has an entry
            continue
        count += 1
        edit_bmml(bmml)

    print()
    if count == 0:
        print("No new files, all bmml files have these entries already!")
    else:
        print("That's all of them. now what do you want to do?")

def edit_bmml(bmml):
    import pdb;pdb.set_trace()
    print()
    print("Regarding \"%s\"'s method types..." % bmml.path)
    cur = bmml.data['method_types'] if 'method_types' in bmml.data else ["GET"]
    if 'method_types' in bmml.data:
        print(" (current method types: %s)" % cur)
    get = utils.prompt_yn("Should GET be a method type?",
            "GET" in cur)
    post = utils.prompt_yn("Should POST be a method type?",
            "POST" in cur)
    put = utils.prompt_yn("Should PUT be a method type?",
            "PUT" in cur)
    delete = utils.prompt_yn("Should DELETE be a method type?",
            "DELETE" in cur)
    mtypes = []
    if get:
        mtypes.append("GET")
    if post:
        mtypes.append("POST")
    if put:
        mtypes.append("PUT")
    if delete:
        mtypes.append("DELETE")


    print()
    print("Regarding \"%s\"'s return types..." % bmml.path)
    cur = bmml.data['return_types'] if 'return_types' in bmml.data else ["HTML"]
    if 'return_types' in bmml.data:
        print(" (current return types: %s)" % cur)
    html = utils.prompt_yn("Should HTML be a return type?",
            "HTML" in cur)
    json = utils.prompt_yn("Should JSON be a return type?",
            "JSON" in cur)
    xml = utils.prompt_yn("Should XML be a return type?",
            "XML" in cur)
    rtypes = []
    if html:
        rtypes.append("HTML")
    if json:
        rtypes.append("JSON")
    if xml:
        rtypes.append("XML")

    bmml.data['method_types'] = mtypes
    bmml.data['return_types'] = rtypes
    print(utils.split_lines("So file %s is going to serve these method types: %s and have these return types: %s" % (bmml.path, mtypes, rtypes)))
    print("Got it, moving on...")

def choose_files(all_bmmls):
    # Build the menu
    options = []
    for b in all_bmmls:
        options.append(
                "%s\n%s\t%s" % (
                    b.path, 
                    b.data['method_types'] if 'method_types' in b.data else "(undef)",
                    b.data['return_types'] if 'return_types' in b.data else "(undef)",
                    )
                )

    print()
    print("Choose which BMML file you want to edit")
    choice = utils.prompt_choices(options)
    edit_bmml(all_bmmls[choice])

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
