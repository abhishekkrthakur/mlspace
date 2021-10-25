import argparse

from .. import __version__
from .create import CreateMLSpaceCommand


def main():
    parser = argparse.ArgumentParser(
        "MLSpace CLI",
        usage="mlspace <command> [<args>]",
        epilog="For more information about a command, run: `mlspace <command> --help`",
    )
    parser.add_argument("--version", "-v", help="Display MLSpace version", action="store_true")

    commands_parser = parser.add_subparsers(help="commands")
    CreateMLSpaceCommand.register_subcommand(commands_parser)

    args = parser.parse_args()

    if args.version:
        print(__version__)
        exit(0)

    if not hasattr(args, "func"):
        parser.print_help()
        exit(1)

    command = args.func(args)
    command.execute()


if __name__ == "__main__":
    main()
