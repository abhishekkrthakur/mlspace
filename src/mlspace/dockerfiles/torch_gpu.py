DOCKERFILE = """
FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Oslo

RUN apt-get update
RUN apt-get install -y \
    build-essential \
    cmake \
    curl \
    gcc \
    git \
    wget \
    sudo \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fOL https://github.com/cdr/code-server/releases/download/v3.12.0/code-server_3.12.0_amd64.deb
RUN dpkg -i code-server_3.12.0_amd64.deb

RUN mkdir -p /workspace
WORKDIR /workspace

RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /workspace
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

ENV HOME=/home/user
RUN chmod 777 /home/user
"""
