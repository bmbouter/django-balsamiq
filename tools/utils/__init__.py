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
        user_input = raw_input("> ")

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
