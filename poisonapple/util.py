"""poisonapple.util"""

import os
import sys
import crayons
import launchd

STATUS_MESSAGES = {
    'failure':          '[!] Failure! The persistence mechansim action failed',
    'python_error':     '[-] Error! Traceback',
    'missing_command':  '[-] Error! Need to specifiy either --command <COMMAND> OR --popup',
    'missing_option':   '[-] Error! Missing required option, see --help for more info...',
    'success':          '[+] Success! The persistence mechanism action was successful',
}

STATUS_COLORS = {
    '[+]': crayons.green,
    '[-]': crayons.red,
    '[!]': crayons.magenta,
    '[~]': crayons.yellow,
}


def print_error(name, text=str(), stop=False):
    message = STATUS_MESSAGES[name]
    if text:
        message += f': {text}'
    for log_type, color in STATUS_COLORS.items():
        if message.startswith(log_type):
            print(color(message))
    if stop:
        sys.exit(1)


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


def get_trigger_command(technique_name):
    directory = os.path.abspath(os.path.dirname(__file__))
    trigger = os.path.join(directory, 'trigger/poisonapple.sh')
    return f'{trigger} {technique_name}'
