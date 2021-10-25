set -e

rm -rf $HOME/.mlspace/

sudo apt-get update
sudo apt-get install -y\
    build-essential\
    git\
    zlib1g-dev\
    libncurses5-dev\
    libgdbm-dev\
    libnss3-dev\
    libssl-dev\
    libreadline-dev\
    libffi-dev\
    libsqlite3-dev\
    wget\
    libbz2-dev

mkdir -p $HOME/.mlspace

cd $HOME/.mlspace
wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz
tar xf Python-3.8.0.tgz
cd Python-3.8.0
./configure --enable-optimizations
make -j 8
sudo make altinstall

cd $HOME/.mlspace
git clone https://github.com/abhishekkrthakur/mlspace.git
cd mlspace && python3.8 setup.py install
cd ..
rm -rf Python-3.8.0.tgz
cp -r mlspace/dockerfiles .
cp -r mlspace/scripts .
cd
