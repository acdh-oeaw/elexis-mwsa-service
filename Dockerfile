FROM python:3.8-buster

ARG GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
RUN echo GOOGLE_APPLICATION_CREDENTIALS
RUN apt-get update
RUN apt install -y git

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN python3 -m nltk.downloader wordnet

COPY . /usr/src/app
RUN git init
RUN ls -la
RUN git status
RUN dvc pull

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]
