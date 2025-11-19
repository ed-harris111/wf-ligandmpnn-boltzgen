# DO NOT CHANGE -- latch base for cuda
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04
#latch stuff
COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:cb01-main /bin/flytectl /bin/flytectl
WORKDIR /root

#FIX INSTALLING AWS CLI

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    apt-get update && apt-get install -y unzip && \
    unzip /tmp/awscliv2.zip -d /tmp && \
    /tmp/aws/install && \
    rm -rf /tmp/aws /tmp/awscliv2.zip


ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev build-essential procps rsync openssh-server

COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main /root/Makefile /root/Makefile
COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main /root/flytekit.config /root/flytekit.config

#setting up python 3.9 and latch stuff
RUN apt-get install -y software-properties-common &&\
    add-apt-repository -y ppa:deadsnakes/ppa &&\
    apt-get install -y python3.9 python3-pip python3.9-distutils curl
    

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /root/miniconda && \
    rm miniconda.sh

RUN /root/miniconda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    /root/miniconda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Install ProteinMPNN environment with conda 
RUN /root/miniconda/bin/conda create --name mlfold python=3.11 -y && \
    /root/miniconda/bin/conda run --name mlfold conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia -y
COPY requirements.txt /opt/latch/requirements.txt
RUN /root/miniconda/bin/conda run --name mlfold pip install --requirement /opt/latch/requirements.txt

env TZ='Etc/UTC'
env LANG='en_US.UTF-8'

arg DEBIAN_FRONTEND=noninteractive

# Latch SDK
# DO NOT REMOVE
RUN pip install --no-cache-dir --upgrade pip latch
RUN pip install 'urllib3>=1.26.0,<2.0.0' --force-reinstall



# Copy workflow data (use .dockerignore to skip files)
copy . /root/
ARG tag
# DO NOT CHANGE
ENV FLYTE_INTERNAL_IMAGE $tag

WORKDIR /root