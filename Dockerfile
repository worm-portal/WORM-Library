# Dockerfile for WORM-Library testing environment
# Includes eq3_6, aqequil, pychnosz, and all dependencies

FROM python:3.12-slim

# Install system dependencies for eq3_6 compilation and Jupyter
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Build and install eq3_6
WORKDIR /tmp/eq3_6
RUN git clone https://github.com/39alpha/eq3_6.git . \
    && make \
    && make install \
    && cd / \
    && rm -rf /tmp/eq3_6

# Set eq3_6 environment variables
# Adjust these paths based on where 'make install' puts files
ENV EQ36DA=/usr/local/share/eq36/data \
    EQ36CO=/usr/local/share/eq36

# Install Python scientific computing packages
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    scipy \
    jupyter \
    jupyterlab \
    ipywidgets \
    papermill \
    nbconvert

# Install WORM packages from GitHub
# aqequil
RUN git clone https://github.com/worm-portal/aqequil.git /opt/aqequil \
    && pip install --no-cache-dir /opt/aqequil

# pychnosz
RUN pip install --no-cache-dir pychnosz

# aqorg (if needed)
RUN git clone https://github.com/worm-portal/aqorg.git /opt/aqorg \
    && pip install --no-cache-dir /opt/aqorg

# complicator (if needed)
RUN git clone https://github.com/worm-portal/complicator.git /opt/complicator \
    && pip install --no-cache-dir /opt/complicator

# propfit (if needed)
RUN git clone https://github.com/worm-portal/propfit.git /opt/propfit \
    && pip install --no-cache-dir /opt/propfit

# Create working directory
WORKDIR /workspace

# Default command
CMD ["/bin/bash"]
