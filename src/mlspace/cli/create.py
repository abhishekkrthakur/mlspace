from argparse import ArgumentParser

from . import BaseCommand


def create_mlspace_command_factory(args):
    return CreateMLSpaceCommand(args.name, args.backend, args.gpus)


class CreateMLSpaceCommand(BaseCommand):
    @staticmethod
    def register_subcommand(parser: ArgumentParser):
        _parser = parser.add_parser("create", help="Create a new MLSpace")
        _parser.add_argument("--name", help="Name of MLSpace", required=True, type=str)
        _parser.add_argument("--backend", help="MLSpace backend", required=True, type=str)
        _parser.add_argument("--gpus", help="Number of GPUs to use", required=True, type=int)
        _parser.set_defaults(func=create_mlspace_command_factory)

    def __init__(self, name, backend, gpus):
        self.name = name
        self.backend = backend
        self.gpus = gpus

    def execute(self):
        from ..mlspace import MLSpace

        mls = MLSpace(name=self.name, backend=self.backend, gpus=self.gpus)
        mls.create_space()
