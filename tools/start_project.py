from __future__ import print_function

import json
import os
import os.path
import sys

import utils
import utils.checks

usage = """
start_project.py - creates a new django-balsamic project

Usage: start_project.py <bmml path>

bmml path
    This is the path to your Balsamic project

start_project.py will create the django-balsamic project in the current
directory.

"""

def main(args):
    """Entry point. args should be a list of length 1 or 2 where item 0 is the
    bmml path and item 1 is the output dir

    """
    out = {}

    try:
        out['bmml_path'] = args[0]
    except IndexError:
        print(usage)
        print()
        print("You must specify the bmml path")
        sys.exit(1)

    out['name'] = utils.prompt_user("What is the name of this project (which"
            " will become the name of the resulting Django app)?",
            checks=[utils.checks.identifier],
            )

    # write out project.json
    outdir = os.getcwd()
    outfile = open(os.path.join(outdir, "project.json"), "w")
    json.dump(out, outfile)
    outfile.write("\n")
    outfile.close()

    print("Output written to project.json")
    print("Done!")

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
