"""poisonapple.util"""

import os
import crayons
import launchd

STATUS_MESSAGES = {
    'failure':          '[!] Failure! The persistence mechansim action failed',
    'python_error':     '[-] Error! Traceback',
    'missing_command':  '[-] Error! Need to specifiy either --command <COMMAND> OR --popup',
    'missing_option':   '[-] Error! Missing required option, see --help for more info...',
    'success':          '[+] Success! The persistence mechanism action was successful',
}


def print_error(name, text=str()):
    message = STATUS_MESSAGES[name]
    if text:
        message += f': {text}'
    if message.startswith('[+]'):
        message_with_color = crayons.green(message)
    elif message.startswith('[-]'):
        message_with_color = crayons.red(message)
    elif message.startswith('[!]'):
        message_with_color = crayons.magenta(message)
    elif message.startswith('[~]'):
        message_with_color = crayons.yellow(message)
    else:
        message_with_color = crayons.white(message)
    print(message_with_color)


def write_plist(label, program_arguments, scope):
    plist = dict(
        Label=label,
        ProgramArguments=program_arguments.split(),
        RunAtLoad=True,
        KeepAlive=True,
    )
    job = launchd.LaunchdJob(label)
    fname = launchd.plist.write(label, plist, scope)
    launchd.load(fname)


def uninstall_plist(label, scope):
    fname = launchd.plist.discover_filename(label, scope)
    if not fname:
        raise Exception(f'{label}.plist not found.')
    launchd.unload(fname)
    os.unlink(fname)


def get_popup_command(technique_name):
    directory = os.path.abspath(os.path.dirname(__file__))
    popup = os.path.join(directory, 'bin/popup.bin')
    return f'{popup} {technique_name}'
