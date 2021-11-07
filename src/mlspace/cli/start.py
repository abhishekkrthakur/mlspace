from argparse import ArgumentParser

from . import BaseCommand


def start_mlspace_command_factory(args):
    return StartMLSpaceCommand(args.name, args.path)


class StartMLSpaceCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("start", help="Start a new space")
        _parser.add_argument(
            "--name",
            help="Name of the MLSpace instance",
            required=True,
        )
        _parser.add_argument(
            "--path",
            help="Path to the code folder",
            required=True,
        )
        _parser.set_defaults(func=start_mlspace_command_factory)

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def execute(self):
        from ..mlspace import MLSpace

        mls = MLSpace()
        mls.start(name=self.name, folder_path=self.path)
