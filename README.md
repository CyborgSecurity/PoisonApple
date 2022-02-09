# PoisonApple

<img src="https://i.imgur.com/Ty5esFJ.png" align="right">

This is a command-line tool to perform various persistence mechanism techniques on macOS. This tool was designed to be used by threat hunters for cyber threat emulation purposes.

## Install

Do it up:
```
$ pip3 install poisonapple --user
```

Note: PoisonApple was written & tested using Python 3.9, it should work using Python 3.6+

## Important Notes!

* PoisonApple will make modifications to your macOS system, it's advised to only use PoisonApple on a virtual machine. Although any persistence mechanism technique added using this tool can also be easily removed (-r), **please use with caution**!
* Be advised: This tool will likely cause common AV / EDR / other macOS security products to generate alerts.
* To understand how any of these techniques work in-depth please see [The Art of Mac Malware, Volume 1: Analysis - Chapter 0x2: Persistence](https://taomm.org/PDFs/vol1/CH%200x02%20Persistence.pdf) by Patrick Wardle of Objective-See. It's a fantastic resource.

## Usage

See PoisonApple switch options (--help):
```
$ poisonapple --help
usage: poisonapple [-h] [-l] [-t TECHNIQUE] [-n NAME] [-c COMMAND] [-r]

Command-line tool to perform various persistence mechanism techniques on macOS.

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            list available persistence mechanism techniques
  -t TECHNIQUE, --technique TECHNIQUE
                        persistence mechanism technique to use
  -n NAME, --name NAME  name for the file or label used for persistence
  -c COMMAND, --command COMMAND
                        command(s) to execute for persistence
  -r, --remove          remove persistence mechanism
```

List of available techniques:
```
$ poisonapple --list
      ,       _______       __
  .-.:|.-.   |   _   .-----|__|-----.-----.-----.
.'        '. |.  |   |  |  |  |__ --|  |  |  |  |
'-."~".  .-' |.  ____|_____|__|_____|_____|__|__|
  } ` }  {   |:  |  _______             __
  } } }  {   |::.| |   _   .-----.-----|  |-----.
  } ` }  {   `---' |.  |   |  |  |  |  |  |  -__|
.-'"~"   '-.       |.  _   |   __|   __|__|_____|
'.        .'       |:  |   |__|  |__|
  '-_.._-'         |::.|:. |
                   `--- ---' v0.2.3

+--------------------+
| AtJob              |
+--------------------+
| Bashrc             |
+--------------------+
| Cron               |
+--------------------+
| CronRoot           |
+--------------------+
| Emond              |
+--------------------+
| Iterm2             |
+--------------------+
| LaunchAgent        |
+--------------------+
| LaunchAgentUser    |
+--------------------+
| LaunchDaemon       |
+--------------------+
| LoginHook          |
+--------------------+
| LoginHookUser      |
+--------------------+
| LoginItem          |
+--------------------+
| LogoutHook         |
+--------------------+
| LogoutHookUser     |
+--------------------+
| Periodic           |
+--------------------+
| Reopen             |
+--------------------+
| Zshrc              |
+--------------------+
```

Apply a persistence mechanism:
```
$ poisonapple -t LaunchAgentUser -n testing
      ,       _______       __
  .-.:|.-.   |   _   .-----|__|-----.-----.-----.
.'        '. |.  |   |  |  |  |__ --|  |  |  |  |
'-."~".  .-' |.  ____|_____|__|_____|_____|__|__|
  } ` }  {   |:  |  _______             __
  } } }  {   |::.| |   _   .-----.-----|  |-----.
  } ` }  {   `---' |.  |   |  |  |  |  |  |  -__|
.-'"~"   '-.       |.  _   |   __|   __|__|_____|
'.        .'       |:  |   |__|  |__|
  '-_.._-'         |::.|:. |
                   `--- ---' v0.2.3

[+] Success! The persistence mechanism action was successful: LaunchAgentUser
```

If no command is specified (-c) a default trigger command will be used which writes to a file on the Desktop every time the persistence mechanism is triggered:
```
$ cat ~/Desktop/PoisonApple-LaunchAgentUser
Triggered @ Tue Mar 23 17:46:02 CDT 2021 
Triggered @ Tue Mar 23 17:46:13 CDT 2021 
Triggered @ Tue Mar 23 17:46:23 CDT 2021 
Triggered @ Tue Mar 23 17:46:33 CDT 2021 
Triggered @ Tue Mar 23 17:46:43 CDT 2021 
Triggered @ Tue Mar 23 17:46:53 CDT 2021 
Triggered @ Tue Mar 23 17:47:03 CDT 2021 
Triggered @ Tue Mar 23 17:47:13 CDT 2021 
Triggered @ Tue Mar 23 17:48:05 CDT 2021 
Triggered @ Tue Mar 23 17:48:15 CDT 2021
```

Remove a persistence mechanism:
```
$ poisonapple -t LaunchAgentUser -n testing -r
...
```

Use a custom command:
```
$ poisonapple -t LaunchAgentUser -n foo -c "echo foo >> /Users/user/Desktop/foo"
...
```