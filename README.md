# PoisonApple

<img src="https://i.imgur.com/Ty5esFJ.png" align="right">

Command-line tool to perform various persistence mechanism techniques on macOS. This tool was designed to be used by threat hunters for cyber threat emulation purposes.

## Install

Do it up:
```
$ pip install poisonapple --user
```

Note: PoisonApple was written & tested using Python 3.9, it should work using Python 3.6+

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

List of avaiable techniques:
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
                   `--- ---' v0.2.0

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
                   `--- ---' v0.2.0

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

Use a custom command:
```
$ poisonapple -t Cron -n foo -c "echo foo >> /Users/user/Desktop/foo"
...
```

Remove a persistence mechanism:
```
$ poisonapple -t LaunchAgentUser -n testing -r
...
```