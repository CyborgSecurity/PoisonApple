"""poisonapple.util"""

import os
import launchd


def write_plist(label, program_arguments, scope):
    plist = dict(
        Label=label,
        ProgramArguments=program_arguments,
        RunAtLoad=True,
        KeepAlive=True,
    )
    job = launchd.LaunchdJob(label)
    fname = launchd.plist.write(label, plist, scope=2)
    launchd.load(fname)


def get_popup_command(technique_name):
    directory = os.path.abspath(os.path.dirname(__file__))
    popup = os.path.join(directory, 'bin/popup.bin')
    return f'{popup} {technique_name}'
