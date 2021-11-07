from argparse import ArgumentParser

from . import BaseCommand


def stop_mlspace_command_factory(args):
    return StopMLSpaceCommand(args.name)


class StopMLSpaceCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("stop", help="Stop a running MLSpace instance")
        _parser.add_argument(
            "--name",
            help="Name of the MLSpace instance",
            required=True,
        )
        _parser.set_defaults(func=stop_mlspace_command_factory)

    def __init__(self, name):
        self.name = name

    def execute(self):
        from ..mlspace import MLSpace

        mls = MLSpace()
        mls.stop(name=self.name)
