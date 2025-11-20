# DO NOT CHANGE 
FROM nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04 #cuda base image 

#latch stuff
COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:cb01-main /bin/flytectl /bin/flytectl
WORKDIR /root


ENV VENV /opt/venv
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONPATH /root
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev build-essential procps rsync openssh-server

COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main /root/Makefile /root/Makefile
COPY --from=812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-cuda:fe0b-main /root/flytekit.config /root/flytekit.config

#setting up python 3.9 and latch stuff -- DO NOT CHANGE
RUN apt-get install -y software-properties-common &&\
    add-apt-repository -y ppa:deadsnakes/ppa &&\
    apt-get install -y python3.9 python3-pip python3.9-distutils curl

#installing awscli
RUN python3.9 -m pip install --upgrade pip && python3.9 -m pip install awscli


RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /root/miniconda && \
    rm miniconda.sh

# confirming terms of service 
RUN /root/miniconda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && \
    /root/miniconda/bin/conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

# Install environment with conda -- Use this for where the pip install model happens 
COPY requirements.txt /opt/latch/requirements.txt    
RUN /root/miniconda/bin/conda create --name mlfold python=3.12 -y && \
    /root/miniconda/bin/conda run --name mlfold pip install --requirement /opt/latch/requirements.txt && \
    /root/miniconda/bin/conda run --name mlfold conda install pytorch-cuda=12.1 -c pytorch -c nvidia -y


#fixing no python issue (there is a chance this can be removed)
env PATH /root/miniconda/envs/mlfold/bin:$PATH

env TZ='Etc/UTC'
env LANG='en_US.UTF-8'

arg DEBIAN_FRONTEND=noninteractive

# Latch SDK
# DO NOT REMOVE
RUN apt-get update && apt-get install -y \
    python3.9 python3.9-dev python3-pip python3.9-distutils curl \
    build-essential libattr1-dev attr
RUN pip install --no-cache-dir --upgrade latch
RUN pip install 'urllib3>=1.26.0,<2.0.0' --force-reinstall
RUN ls /root/miniconda/bin/conda




# Copy workflow data (use .dockerignore to skip files)
copy . /root/
ARG tag

# DO NOT CHANGE
ENV FLYTE_INTERNAL_IMAGE $tag

WORKDIR /root