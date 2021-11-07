import os
import subprocess
import sys

from .dockerfiles import TORCH_GPU
from .logger import logger
from .requirements import BASE_REQUIREMENTS
from getpass import getpass
import tempfile

from .scripts import install_docker, install_nvidia_docker, install_nvidia_drivers, base_script


class MLSpace:
    def __init__(self) -> None:
        self.home_dir = os.path.expanduser("~")
        self.dockerfiles_dir = os.path.join(self.home_dir, ".mlspace/dockerfiles")

    def create_space(self, name: str, backend: str, gpu: bool):
        self._create_required_folders(name=name)
        self._build_container(name=name, backend=backend, gpu=gpu)
        logger.info(f"Created space {name}")

    def _build_container(self, name, backend, gpu):
        if backend == "torch" and gpu is True:
            docker_file = "Dockerfile.torch.gpu"
            requirements_file = "requirements.torch.gpu"
            docker_file_path = os.path.join(self.home_dir, f".mlspace/dockerfiles/{docker_file}")
            requirements_path = os.path.join(self.home_dir, f".mlspace/dockerfiles/{requirements_file}")
            with open(docker_file_path, "w") as f:
                f.write(TORCH_GPU.strip())
            with open(requirements_path, "w") as f:
                f.write(BASE_REQUIREMENTS.strip())
        else:
            logger.error(f"Unknown backend: {backend}")
            sys.exit(1)

        command1 = f"docker build -t {name} --build-arg requirements={requirements_file}"
        command2 = f"-f {docker_file_path} {self.dockerfiles_dir}"
        command = f"{command1} {command2}"
        logger.info(f"Building space `{name}`. This may take a while...")
        self._run_command(command)
        logger.info(f"Space `{name}` successfully built.")

    def _create_required_folders(self, name):
        logger.info(f"Creating required folders for space `{name}`")
        os.makedirs(f"{self.home_dir}/.mlspace", exist_ok=True)
        os.makedirs(f"{self.home_dir}/.mlspace/dockerfiles", exist_ok=True)
        os.makedirs(f"{self.home_dir}/.mlspace/{name}", exist_ok=True)
        """
        if not os.path.exists(f"{self.home_dir}/.mlspace/{name}"):
            os.makedirs(f"{self.home_dir}/.mlspace/{name}", exist_ok=False)
            os.makedirs(f"{self.home_dir}/.mlspace/{name}/logs", exist_ok=False)
        else:
            logger.error(f"This mlspace already exists. Please choose a different name or delete the space.")
            exit(1)
        """

    @staticmethod
    def _run_command(command, password=None, ignore_errors=False):
        proc = subprocess.Popen(command.strip().split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if password is None:
            _, err = proc.communicate()
        else:
            _, err = proc.communicate(password.encode())
        if err and ignore_errors is False:
            logger.error(command)
            logger.error(err)
            sys.exit(1)

    def setup(self, version=470):
        install_script = os.path.join(self.home_dir, ".mlspace/installer.sh")
        with open(install_script, "w") as f:
            f.write(base_script)
            f.write("\n")
            f.write(install_docker.strip())
            f.write("\n")
            f.write(install_nvidia_docker.strip())
            f.write("\n")
            f.write(install_nvidia_drivers.strip().format(version=version))
        command = f"sudo sh {install_script}"
        subprocess.run(command.split(), stderr=sys.stderr, stdout=sys.stdout)
        logger.info("Setup complete")
        logger.info("Now, it would be a nice idea to restart your computer :)")

    def stop(self, name: str):
        command = f"docker stop {name}_code"
        self._run_command(command)

        command = f"docker rm {name}_code"
        self._run_command(command)

        command = f"docker stop {name}_lab"
        self._run_command(command)

        command = f"docker rm {name}_lab"
        self._run_command(command)

        logger.info(f"Space {name} stopped")

    def start(self, name, folder_path, coder_port=15000, lab_port=15001):
        logger.info(f"Starting space {name} on {folder_path}")
        # extract password from yaml file
        # with open(f"{folder_path}/config.yaml", "r") as f:
        #    config = yaml.safe_load(f)
        #    password = config["password"]
        # get user id and group id
        user_id = os.getuid()
        group_id = os.getgid()
        password = "abhishek"

        command1 = f"docker run --name {name}_code -itd -u {user_id}:{group_id} -e PASSWORD={password}"
        command2 = f"-p {coder_port}:3000 -v {folder_path}:/workspace {name}"
        command3 = "code-server /workspace --bind-addr 0.0.0.0:3000"
        command = f"{command1} {command2} {command3}"
        self._run_command(command)

        command1 = f"docker run --name {name}_lab -itd -u {user_id}:{group_id} -e PASSWORD={password}"
        command2 = f"-p {lab_port}:3001 -v {folder_path}:/workspace {name}"
        command3 = "jupyter-lab /workspace --ip='*' --port 3001 --no-browser"
        command4 = "--NotebookApp.token='' --NotebookApp.password=''"
        command = f"{command1} {command2} {command3} {command4}"
        self._run_command(command)
