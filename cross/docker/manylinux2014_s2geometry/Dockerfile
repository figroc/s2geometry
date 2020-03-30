FROM quay.io/pypa/manylinux2014_x86_64
LABEL maintainer="Cheng Chi<cheng-chi@outlook.com>"

# install openssl, swig, wget
RUN yum install -y swig3 \
  && yum install -y openssl-static \
  && yum install -y wget

# install cmake 3.17
RUN wget -qO- "https://cmake.org/files/v3.17/cmake-3.17.0-Linux-x86_64.tar.gz" \
  | tar --strip-components=1 -xz -C /usr/local

# install miniconda
RUN mkdir conda_install \
  && cd conda_install \
  && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
  && chmod +x Miniconda3-latest-Linux-x86_64.sh \
  && ./Miniconda3-latest-Linux-x86_64.sh -b \
  && cd .. \
  && rm -rf conda_install \
  && eval "$(~/miniconda3/bin/conda shell.bash hook)" \
  && conda update -n base -c defaults conda \
  && conda init 

# create python conda enviroments
RUN eval "$(~/miniconda3/bin/conda shell.bash hook)" \
  && conda create -n py35 python=3.5 -y \
  && conda create -n py36 python=3.6 -y \
  && conda create -n py37 python=3.7 -y \
  && conda create -n py38 python=3.8 -y

# default shell
CMD ["/bin/bash"]
