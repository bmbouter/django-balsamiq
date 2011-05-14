import re

"""
This module defines a number of check functions for use in utils.prompt. They
each take a string and return True or False. If they return False indicating
the string is rejected, they should print a reason for the failure.
"""

def not_empty(s):
    if not s.strip():
        print("Must not be empty")
        return False
    return True

ident_re = re.compile("[a-z][a-z0-9_]*")
def identifier(s):
    """lowercase alphanumeric + underscore, starts with a letter, at least 1
    char long"""
    if not ident_re.match(s):
        print("Answer must consist of letters, numbers, and the underscore and must start\nwith a letter")
        return False
    return True

def yn(s):
    if s.lower() not in ("y", "yes", "n", "no", ""):
        print("Please answer yes or no")
        return False
    return True
