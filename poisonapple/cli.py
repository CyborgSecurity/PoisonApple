"""poisonapple.cli"""

import crayons
import argparse

BANNER = '''
      ,       _______       __
  .-.:|.-.   |   .   .-----|__.-----.-----.-----.
.'        '. |.  |   |  -  |  |__ --|  -  |     |
'-."~".  .-' |.  ____|_____|__|_____|_____|__|__|
  } ` }  {   |:  | _______             __
  } } }  {   |::.||   _   .-----.-----|  |-----.
  } ` }  {   `---'|.  |   |  -  |  -  |  |  -__|
.-'"~"   '-.      |.  _   |   __|   __|__|_____|
'.        .'      |:  |   |__|  |__|
  '-_.._-'        |::.|:. |
                  `--- ---' v0.1.0
'''


def get_parser():
    parser = argparse.ArgumentParser(
        description='Command-line tool to perform various persistence mechanism techniques on macOS.'
    )
    parser.add_argument(
        '-v', '--version',
        action='store_true',
        help='display the current version'
    )
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print('v0.1.0'); return

    print(BANNER)


if __name__ == '__main__':
    main()