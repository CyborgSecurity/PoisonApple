"""poisonapple.util"""

import os
import crayons
import launchd

STATUS_MESSAGES = {
    'failure':          '[!] Failure! The persistence mechansim failed...',
    'python_error':     '[-] Error! Traceback...',
    'missing_command':  '[-] Error! Need to specifiy either --command <COMMAND> OR --popup',
    'missing_option':   '[-] Error! Missing required option, see --help for more info...',
    'success':          '[+] Success! The persistence mechanism was applied...',
}


def print_error(name, text=str()):
    message = ' '.join([STATUS_MESSAGES[name], text]).strip()
    if message.startswith('[+]'):
        print(crayons.green(message))
    elif message.startswith('[-]'):
        print(crayons.red(message))
    elif message.startswith('[!]'):
        print(crayons.magenta(message))
    elif message.startswith('[~]'):
        print(crayons.yellow(message))
    else:
        print(crayons.white(message))


def write_plist(label, program_arguments, scope):
    plist = dict(
        Label=label,
        ProgramArguments=program_arguments.split(),
        RunAtLoad=True,
        KeepAlive=True,
    )
    job = launchd.LaunchdJob(label)
    fname = launchd.plist.write(label, plist, scope=scope)
    launchd.load(fname)


def get_popup_command(technique_name):
    directory = os.path.abspath(os.path.dirname(__file__))
    popup = os.path.join(directory, 'bin/popup.bin')
    return f'{popup} {technique_name}'
