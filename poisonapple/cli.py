"""poisonapple.cli"""

import argparse

from poisonapple.techniques import technique_list

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
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    print(BANNER)

    if args['list']:
        seperator = f'+{"-"*40}+'
        for technique in technique_list:
            print(f'{seperator}\n| {technique.name:<38} |')
        print(seperator)
        return

    for technique in technique_list:
        if technique.name.strip().lower() in args['technique'].strip().lower():
            technique.run()


if __name__ == '__main__':
    main()