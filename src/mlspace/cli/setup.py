from argparse import ArgumentParser

from . import BaseCommand


def setup_mlspace_command_factory(args):
    return SetupMLSpaceCommand()


class SetupMLSpaceCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("install", help="Setup MLSpace and install all dependencies. Run with `sudo`")
        _parser.set_defaults(func=setup_mlspace_command_factory)

    def execute(self):
        from ..mlspace import MLSpace

        mls = MLSpace()
        mls.setup()
