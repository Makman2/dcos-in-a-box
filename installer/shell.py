from subprocess import Popen, PIPE


def bash(cmd, stdin=''):
    print(cmd)
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    if stdin:
        return p.communicate(stdin)
    else:
        return p.communicate()

yes_phrases = {'yes', 'yeah', 'y'}
no_phrases = {'no', 'nope', 'n'}

def ask_for_permission():
    """
    Asks the user for permission on terminal.

    :return: If the user enters a yes-phrase, `True` is returned. If the
             users enters a no-phrase, `False` is returned. If an unrecognized
             phrase is entered, `None` is returned.
    """
    while True:
        answer = input().strip()
        if answer in yes_phrases:
            return True
        elif answer in no_phrases:
            return False
        else:
            print("Please enter {} or {}:".format(', '.join(yes_phrases), ', '.join(no_phrases)))
