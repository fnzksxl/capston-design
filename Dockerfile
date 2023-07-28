ARG PYTORCH="1.13.0"
ARG CUDA="11.6"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

# # To fix GPG key error when running apt-get update
# RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub \
#     && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# Install system dependencies for opencv-python
# RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
COPY requirements.txt .

ENV PYTHONUNBUFFERED=True \
    PIP_CACHE_DIR=/.cache
ENV  GIT_PYTHON_REFRESH=quiet

RUN --mount=type=cache,target=$PIP_CACHE_DIR \
    pip install -r requirements.txt

WORKDIR /app
RUN mkdir saved_model

COPY *.py .
COPY dataset/data.tsv .
COPY saved_model /app/saved_model/