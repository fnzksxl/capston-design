ARG PYTORCH="1.13.0"
ARG CUDA="11.6"
ARG CUDNN="8"

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

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
COPY saved_model /app/saved_model/
COPY dataset /app/dataset/