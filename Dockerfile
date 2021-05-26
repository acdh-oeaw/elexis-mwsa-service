# syntax = docker/dockerfile:experimental
FROM python:3.8-buster

RUN apt-get update
RUN apt install -y git

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN python3 -m nltk.downloader wordnet
RUN python3 swagger_server/language_model_install.py

COPY . /usr/src/app

RUN git init
RUN ls -la
RUN git status

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
