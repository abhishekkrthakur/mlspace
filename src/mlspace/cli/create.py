from argparse import ArgumentParser

from ..utils import SUPPORTED_BACKENDS
from . import BaseCommand


def create_mlspace_command_factory(args):
    return CreateMLSpaceCommand(args.name, args.backend, args.gpu)


class CreateMLSpaceCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("create", help="Create a new MLSpace")
        _parser.add_argument(
            "--name",
            help="Name of MLSpace",
            required=True,
            type=str,
        )
        _parser.add_argument(
            "--backend",
            help="MLSpace backend",
            required=True,
            type=str,
            choices=SUPPORTED_BACKENDS,
        )
        _parser.add_argument(
            "--gpu",
            help="Whether to use GPU",
            action="store_true",
            required=False,
        )
        _parser.set_defaults(func=create_mlspace_command_factory)

    def __init__(self, name, backend, gpu):
        self.name = name
        self.backend = backend
        self.gpu = gpu

    def execute(self):
        from ..mlspace import MLSpace

        mls = MLSpace()
        mls.create_space(name=self.name, backend=self.backend, gpu=self.gpu)
