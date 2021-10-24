#!/usr/bin/env bash

set -e

sudo add-apt-repository -y ppa:graphics-drivers/ppa
sudo apt-get install -y nvidia-driver-470
