import os
import sys
import crayons
import launchd
import plistlib

from crontab import CronTab

STATUS_MESSAGES = {
    "failure": "[!] Failure! The persistence mechansim action failed",
    "python_error": "[-] Error! Traceback",
    "missing_command": "[-] Error! Need to specifiy either --command <COMMAND> OR --popup",
    "missing_option": "[-] Error! Missing required option, see --help for more info...",
    "success": "[+] Success! The persistence mechanism action was successful",
    "warning": "[~] Warning",
}

STATUS_COLORS = {
    "[+]": crayons.green,
    "[-]": crayons.red,
    "[!]": crayons.magenta,
    "[~]": crayons.yellow,
}


def print_status(name, text=str(), stop=False):
    message = STATUS_MESSAGES[name]
    if text:
        message += f": {text}"
    for log_type, color in STATUS_COLORS.items():
        if message.startswith(log_type):
            print(color(message))
    if stop:
        sys.exit(1)


def get_full_path(relative_path):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), relative_path)


def get_plist(file_path):
    with open(file_path, "rb") as f:
        return plistlib.load(f)


def write_plist(file_path, data):
    with open(file_path, "wb") as f:
        plistlib.dump(data, f)


def plist_launch_write(label, program_arguments, scope):
    plist = dict(
        Label=label,
        ProgramArguments=program_arguments.split(),
        RunAtLoad=True,
        KeepAlive=True,
    )
    job = launchd.LaunchdJob(label)
    fname = launchd.plist.write(label, plist, scope)
    launchd.load(fname)


def plist_launch_uninstall(label, scope):
    fname = launchd.plist.discover_filename(label, scope)
    if not fname:
        raise Exception(f"{label}.plist not found.")
    launchd.unload(fname)
    os.unlink(fname)


def get_trigger_command(technique_name):
    return f'{get_full_path("auxiliary/poisonapple.sh")} {technique_name}'


def create_cron_job(user, command, comment):
    cron = CronTab(user=user)
    job = cron.new(command=command, comment=comment)
    job.minute.every(1)
    cron.write()


def remove_line(string, file_path):
    lines = list()
    with open(file_path) as f:
        for line in f.readlines():
            if string in line:
                continue
            lines.append(line)
    with open(file_path, "w") as f:
        for line in lines:
            f.write(line)


def create_app(name, command, technique_name):
    auxiliary_path = get_full_path("auxiliary/")
    app_path = os.path.join(auxiliary_path, f"{name}.app")
    app_path_full = os.path.join(app_path, "Contents/MacOS")
    try:
        os.makedirs(app_path_full)
    except FileExistsError:
        pass
    app_path_script = os.path.join(app_path_full, name)
    with open(app_path_script, "w") as f:
        f.write(f"#!/usr/bin/env bash\n{command}")
    os.chmod(app_path_script, 0o755)
    return app_path
