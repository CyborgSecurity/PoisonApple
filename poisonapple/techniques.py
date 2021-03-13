"""poisonapple.techniques"""

import os

from poisonapple.util import print_error, write_plist


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
        write_plist(self.name, self.command, scope=2)


class LaunchDaemon(Technique):
    def __init__(self, name, command):
        super().__init__('LaunchDaemon', name, command, root_required=True)

    @Technique.execute
    def run(self):
        write_plist(self.name, self.command, scope=3)


technique_list = [
    LaunchAgent,
    LaunchDaemon,
]