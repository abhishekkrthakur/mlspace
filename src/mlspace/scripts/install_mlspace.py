script = """
set -e

sudo apt-get update

sudo apt-get install -y python3 python3-pip
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

pip install -U pip
pip install -U mlspace
"""
