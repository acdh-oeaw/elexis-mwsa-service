# syntax = docker/dockerfile:experimental
FROM python:3.8-buster

RUN apt-get update && \
    apt install -y git && \
    apt install libgit2-dev && \
    mkdir -p /usr/src/app && \
    pip install --upgrade pip setuptools wheel && \
    pip install "dvc[gs]"==2.0.18

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
