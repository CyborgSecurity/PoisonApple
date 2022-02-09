import argparse

from poisonapple.techniques import Technique
from poisonapple.util import get_trigger_command, print_status

BANNER = """\
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
"""


def get_parser():
    parser = argparse.ArgumentParser(
        description="Command-line tool to perform various persistence mechanism techniques on macOS."
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="list available persistence mechanism techniques",
    )
    parser.add_argument(
        "-t",
        "--technique",
        default=str(),
        type=str,
        help="persistence mechanism technique to use",
    )
    parser.add_argument(
        "-n",
        "--name",
        default=str(),
        type=str,
        help="name for the file or label used for persistence",
    )
    parser.add_argument(
        "-c",
        "--command",
        default=str(),
        type=str,
        help="command(s) to execute for persistence",
    )
    parser.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="remove persistence mechanism"
    )
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    technique_list = Technique.__subclasses__()
    print(BANNER)

    if args["list"]:
        seperator = f'+{"-"*20}+'
        for technique in technique_list:
            print(f"{seperator}\n| {technique.__name__:<18} |")
        print(seperator)
        return

    name = args["name"]
    remove = args["remove"]
    command = args["command"]
    technique = args["technique"]

    if not (name and technique):
        print_status("missing_option", stop=True)

    for technique_class in technique_list:
        technique_name = technique_class.__name__
        if technique_name.lower() == technique.strip().lower():
            if not command:
                command = get_trigger_command(technique_name)
            t = technique_class(name, command)
            if remove:
                t.remove()
            else:
                t.run()


if __name__ == "__main__":
    main()
