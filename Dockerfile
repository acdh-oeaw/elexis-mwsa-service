# syntax = docker/dockerfile:experimental
FROM python:3.8-buster

RUN apt-get update && \
    apt install -y git && \
    mkdir -p /usr/src/app

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
