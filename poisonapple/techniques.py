"""poisonapple.techniques"""

import os

from crontab import CronTab
from poisonapple.util import print_error, write_plist, uninstall_plist


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


class LaunchAgent(Technique):
    def __init__(self, name, command):
        super().__init__('LaunchAgent', name, command, root_required=True)

    @Technique.execute
    def run(self):
        write_plist(self.name, self.command, 2)

    @Technique.execute
    def remove(self):
        uninstall_plist(self.name, 2)


class LaunchDaemon(Technique):
    def __init__(self, name, command):
        super().__init__('LaunchDaemon', name, command, root_required=True)

    @Technique.execute
    def run(self):
        write_plist(self.name, self.command, 3)

    @Technique.execute
    def remove(self):
        uninstall_plist(self.name, 3)


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


class AtJob(Technique):
    def __init__(self, name, command):
        super().__init__('AtJob', name, command, root_required=True)

    @Technique.execute
    def run(self):
        os.system('launchctl unload -F /System/Library/LaunchDaemons/com.apple.atrun.plist')
        os.system('launchctl load -w /System/Library/LaunchDaemons/com.apple.atrun.plist')
        # recurisve at command here

    @Technique.execute
    def remove(self):
        pass


"""
# https://github.com/python/cpython/blob/master/Lib/plistlib.py
# might be depreciated
class StartupItems(Technique):
    def __init__(self, name, command):
        super().__init__('LogoutHook', name, command, root_required=True)

    @Technique.execute
    def run(self):
"""


technique_list = [
    AtJob,
    Cron,
    LaunchAgent,
    LaunchDaemon,
    LoginHook,
    LogoutHook,
    Periodic,
]