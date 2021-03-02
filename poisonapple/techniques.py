"""poisonapple.techniques"""

import os
import crayons

from poisonapple.util import write_plist


class Technique:
    def __init__(self, technique, root_required=False):
        self.technique = technique
        self.root_required = root_required
        self.success = False
        self.error_message = str()

    def display_result(self):
        if self.success:
            print(crayons.green(
                f'[+] Success! The {self.technique} persistence mechanism was applied.'
            ))
        else:
            print(crayons.red(
                f'[-] Error! The {self.technique} persistence mechansim failed.\n' + \
                f'[-] {self.error_message}'
            ))

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
        super().__init__('LaunchAgent', root_required=True)
        self.name = name
        self.command = command

    @Technique.execute
    def run(self):
        write_plist(self.name, self.command, scope=2)


class LaunchDaemon(Technique):
    def __init__(self, name, command):
        super().__init__('LaunchDaemon', root_required=True)
        self.name = name
        self.command = command

    @Technique.execute
    def run(self):
        write_plist(self.name, self.command, scope=3)


technique_list = [
    LaunchAgent,
    LaunchDaemon,
]