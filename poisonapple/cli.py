"""poisonapple.cli"""

import argparse

from poisonapple.techniques import technique_list
from poisonapple.util import get_popup_command

BANNER = '''\
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
                   `--- ---' v0.1.1
'''


def get_parser():
    parser = argparse.ArgumentParser(
        description='Command-line tool to perform various persistence mechanism techniques on macOS.'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='list available persistence mechanism techniques'
    )
    parser.add_argument(
        '-t', '--technique',
        default=str(), type=str,
        help='persistence mechanism technique to use'
    )
    parser.add_argument(
        '-n', '--name',
        default=str(), type=str,
        help='name for the file or label used for persistence'
    )
    parser.add_argument(
        '-c', '--command',
        default=str(), type=str,
        help='command(s) to execute for persistence'
    )
    parser.add_argument(
        '-p', '--popup',
        action='store_true',
        help='create a popupbox for testing persistence (use in lieu of a command)'
    )
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    print(BANNER)

    if args['list']:
        seperator = f'+{"-"*20}+'
        for technique in technique_list:
            print(f'{seperator}\n| {technique.__name__:<18} |')
        print(seperator)
        return

    name = args['name']
    command = args['command'].split()

    if not (name or command or args['technique']):
        print('Missing required option, see --help for more info...')
        return

    for technique in technique_list:
        technique_name = technique.__name__
        if technique_name.lower() in args['technique'].strip().lower():
            if not command:
                command = get_popup_command(technique_name)
            t = technique(name, command)
            t.run()


if __name__ == '__main__':
    main()