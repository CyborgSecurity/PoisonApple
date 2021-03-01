"""poisonapple.techniques"""

import crayons


class Technique:
    def __init__(self, name):
        self.name = name
        self.success = False
        self.error_message = str()

    def display_result(self):
        if self.success:
            print(crayons.green(
                f'[+] Success! The {self.name} persistence mechanism was applied.'
            ))
        else:
            print(crayons.red(
                f'[-] Error! The {self.name} persistence mechansim failed.\n' + \
                self.error_message
            ))


class LaunchAgent(Technique):
    def __init__(self):
        super().__init__('LaunchAgent')

    def run(self):
        self.success = True
        self.display_result()


class LaunchDaemon(Technique):
    def __init__(self):
        super().__init__('LaunchDaemon')

    def run(self):
        self.success = True
        self.display_result()


technique_list = [
    LaunchAgent(),
    LaunchDaemon(),
]