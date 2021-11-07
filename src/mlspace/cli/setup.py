from argparse import ArgumentParser

from . import BaseCommand


def setup_mlspace_command_factory(args):
    return SetupMLSpaceCommand()


class SetupMLSpaceCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("setup", help="Setup MLSpace and install all dependencies. Run with `sudo`")
        _parser.add_argument(
            "--generate_install_script",
            help="Adding this argument will just generate the install script. Used in development only.",
            action="store_true",
            required=False,
        )
        _parser.set_defaults(func=setup_mlspace_command_factory)

    def execute(self):
        from ..mlspace import MLSpace

        mls = MLSpace()
        mls.setup()
