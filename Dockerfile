FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libncurses5-dev \
    libncursesw5-dev \
    git \
    curl \
    python3-dev \
    python3-pip

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN CMAKE_ARGS="-DLLAMA_CUDA=on" poetry add llama-cpp-python

COPY . /app

RUN mkdir -p /app/data/complete /app/data/processed /app/data/raw/test /app/data/raw/train

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["poetry", "run", "python", "main.py"]
