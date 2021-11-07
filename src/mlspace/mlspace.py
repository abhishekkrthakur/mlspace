import os
import subprocess
import sys

from .dockerfiles import TORCH_GPU
from .logger import logger


class MLSpace:
    def __init__(self) -> None:
        self.home_dir = os.path.expanduser("~")

    def create_space(self, name: str, backend: str, gpu: bool):
        self._create_required_folders(name=name)
        self._build_container(name=name, backend=backend, gpu=gpu)
        logger.info(f"Created space {name}")

    def _build_container(self, name, backend, gpu):
        if backend == "torch" and gpu is True:
            docker_file = "Dockerfile.torch.gpu"
            with open(f"{self.home_dir}/.mlspace/dockerfiles/{docker_file}", "w") as f:
                f.write(TORCH_GPU.strip())
        else:
            logger.error(f"Unknown backend: {backend}")
            sys.exit(1)

        command = f"docker build -t {name} -f {self.home_dir}/.mlspace/dockerfiles/{docker_file} ."
        print(command)
        logger.info(f"Building space `{name}`. This may take a while...")
        self._run_command(command)
        logger.info(f"Space `{name}` successfully built.")

    def _create_required_folders(self, name):
        logger.info(f"Creating required folders for space `{name}`")
        os.makedirs(f"{self.home_dir}/.mlspace", exist_ok=True)
        os.makedirs(f"{self.home_dir}/.mlspace/dockerfiles", exist_ok=True)
        os.makedirs(f"{self.home_dir}/.mlspace/{name}", exist_ok=True)
        os.makedirs(f"{self.home_dir}/.mlspace/{name}/logs", exist_ok=True)
        """
        if not os.path.exists(f"{self.home_dir}/.mlspace/{name}"):
            os.makedirs(f"{self.home_dir}/.mlspace/{name}", exist_ok=False)
            os.makedirs(f"{self.home_dir}/.mlspace/{name}/logs", exist_ok=False)
        else:
            logger.error(f"This mlspace already exists. Please choose a different name or delete the space.")
            exit(1)
        """

    @staticmethod
    def _run_command(command):
        proc = subprocess.Popen(command.strip().split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, err = proc.communicate()
        if err:
            logger.error(err)
            sys.exit(1)

    def setup(self):
        self._install_docker()
        self._install_nvidia_driver()
        self._install_nvidia_docker()

    def _install_nvidia_driver(self, driver_verison=470):
        # install nvidia drivers
        command = "add-apt-repository -y ppa:graphics-drivers/ppa"
        self._run_command(command)

        command = "apt-get update"
        self._run_command(command)

        command = f"apt-get install -y nvidia-driver-{driver_verison}"
        self._run_command(command)

    def _install_nvidia_docker(self):
        command = """
        distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
        && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
        && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
        sudo tee /etc/apt/sources.list.d/nvidia-docker.list
        """
        self._run_command(command)

        command = "apt-get update"
        self._run_command(command)

        command = "apt-get install -y nvidia-docker2"
        self._run_command(command)

        command = "systemctl restart docker"
        self._run_command(command)

    def _install_docker(self):
        # install docker
        command = "apt-get remove -y docker docker-engine docker.io containerd runc"
        self._run_command(command)

        command = "apt-get update"
        self._run_command(command)

        command = "apt-get install -y ca-certificates curl gnupg lsb-release"
        self._run_command(command)

        command = "rm -rf /usr/share/keyrings/docker-archive-keyring.gpg"
        self._run_command(command)

        command = "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg"
        self._run_command(command)

        command = """
        echo \
            "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
            https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
            tee /etc/apt/sources.list.d/docker.list > /dev/null
        """
        self._run_command(command)

        command = "apt-get update"
        self._run_command(command)

        command = "apt-get install -y docker-ce docker-ce-cli containerd.io"
        self._run_command(command)

        command = "groupadd -f docker"
        self._run_command(command)

        command = "usermod -aG docker $USER"
        self._run_command(command)

        command = "systemctl enable docker.service"
        self._run_command(command)

        command = "systemctl enable containerd.service"
        self._run_command(command)

    def stop(self, name: str):
        command = f"docker stop {name}_code"
        self._run_command(command)

        command = f"docker rm {name}_code"
        self._run_command(command)

    def start(self, name, folder_path, coder_port=15000):
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
