import os
import subprocess
import sys
import uuid
from dataclasses import dataclass

from loguru import logger


@dataclass
class MLSpace:
    name: str
    gpus: int
    backend: str

    def __post_init__(self):
        logger.info(f"MLSpace: {self.name}")
        logger.info(f"GPUs: {self.gpus}")
        logger.info(f"Backend: {self.backend}")
        self.space_identifier = uuid.uuid4()
        self.home_dir = os.path.expanduser("~")

    def create_space(self):
        self._create_required_folders()
        self._build_container()
        logger.info(f"Created space {self.name}")

    def _build_container(self):
        if self.backend == "tf" and self.gpus > 0:
            docker_file = "Dockerfile.tf.gpu"
        elif self.backend == "tf" and self.gpus == 0:
            docker_file = "Dockerfile.tf.cpu"
        elif self.backend == "pt" and self.gpus > 0:
            docker_file = "Dockerfile.pt.gpu"
        elif self.backend == "pt" and self.gpus == 0:
            docker_file = "Dockerfile.pt.cpu"
        elif self.backend == "generic":
            docker_file = "Dockerfile.cpu"
        else:
            logger.error(f"Unknown backend: {self.backend}")
            sys.exit(1)

        command = f"docker build -t {self.name} -f {self.home_dir}/.mlspace/dockerfiles/{docker_file} ."
        proc = subprocess.Popen(command.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f"Building space `{self.name}`. This may take a while...")
        _, err = proc.communicate()
        if err:
            logger.error(err)
            sys.exit(1)
        logger.info(f"Space `{self.name}` successfully built.")

    def _create_required_folders(self):
        os.makedirs(f"{self.home_dir}/.mlspace", exist_ok=True)
        # check if folder self.name exists
        os.makedirs(f"{self.home_dir}/.mlspace/{self.name}", exist_ok=True)
        os.makedirs(f"{self.home_dir}/.mlspace/{self.name}/logs", exist_ok=True)
        """
        if not os.path.exists(f"{self.home_dir}/.mlspace/{self.name}"):
            os.makedirs(f"{self.home_dir}/.mlspace/{self.name}", exist_ok=False)
            os.makedirs(f"{self.home_dir}/.mlspace/{self.name}/logs", exist_ok=False)
        else:
            logger.error(f"This mlspace already exists. Please choose a different name or delete the space.")
            exit(1)
        """
