from __future__ import print_function

import os, os.path
import json
import sys

from . import checks

def split_lines(s, textwidth=80):
    """Takes a string and splits it at word boundaries"""
    parts = []
    while len(s) > textwidth:
        # Find the space 
        index = s.rfind(" ", 0, textwidth)
        parts.append(s[:index].strip())
        s = s[index:]

    parts.append(s.strip())
    return "\n".join(parts)

def split_lines_indent(s, indent, textwidth=80):
    "Indents all lines but the first by indent spaces"
    parts = []
    # Initial split, no indent
    if len(s) > textwidth:
        index = s.rfind(" ", 0, textwidth)
        parts.append(s[:index].strip())
        s = s[index:]

    # further splits, with indent
    while len(s) > textwidth-indent:
        # Find the space 
        index = s.rfind(" ", 0, textwidth-indent)
        parts.append(" "*indent + s[:index].strip())
        s = s[index:]

    if not parts: indent = 0
    parts.append(" "*indent + s.strip())
    return "\n".join(parts)

def prompt_choices(choices):

    num_choices = len(choices)

    def print_menu():
        print("%2s) %s" % (0, split_lines_indent("Show menu again",4)))
        for num, c in enumerate(choices):
            print("%2s) %s" % (num+1, split_lines_indent(c,4)))

    while True:
        print_menu()

        while True:
            choice = int(prompt_user("Enter your choice", checks=[checks.numeric]))

            if choice == 0:
                print_menu()
            elif choice < 1 or choice > num_choices:
                print("Bad choice. Please choose an item from the menu")
            else:
                break

        return choice - 1

    

def prompt_user(prompt, checks=None):
    """Prompts the user for a string. The string must conform to the checks
    given, or the prompt will be re-displayed. Checks should be an interable of
    functions that take a string and return True or False.
    
    See the utils.checks module for pre-written checks to use

    Default is to pass, if no check fails, the string is assumed to pass

    Check functions should print out a string with the reason of failure
    
    """
    if checks is None:
        checks = ()

    prompt = split_lines(prompt)

    while True:
        print(prompt)
        try:
            user_input = raw_input("> ")
        except KeyboardInterrupt:
            print()
            print("Are you sure? If you exit now, you will lose all your changes!")
            result = prompt_yn("Really Quit?", False)
            if result:
                sys.exit(0)
            continue

        failed = False
        # check all checks, even if one fails
        for check in checks:
            if not check(user_input):
                failed = True

        if not failed:
            return user_input
        
def prompt_yn(prompt, defaultyes=True):
    """Prompts for a yes/no answer from the user.
    Returns True - yes
            False - no"""

    if defaultyes:
        yn = "[Y/n]"
    else:
        yn = "[y/N]"

    answer = prompt_user(prompt + " " + yn,
            checks=[checks.yn])
    if not answer:
        return defaultyes

    if answer[0] in "yY":
        return True
    else:
        return False

def find_projectjson(arg):
    """Returns the json object for the project.json"""
    if not arg:
        targetdir = os.getcwd()
    else:
        targetdir = arg

    if os.path.isfile(targetdir):
        targetfile = targetdir
    else:
        if not os.path.isdir(targetdir):
            return False
        targetfile = os.path.join(targetdir, "project.json")

    with open(targetfile, "r") as f:
        return json.load(f)

