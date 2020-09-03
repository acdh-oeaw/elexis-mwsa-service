# syntax = docker/dockerfile:experimental
FROM ubuntu:20.04

RUN apt-get update
#RUN apt install -y curl
#RUN apt-get update && apt-get install -y gnupg2
#RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y
#RUN --mount=type=secret,id=auto-devops-build-secrets . /run/secrets/auto-devops-build-secrets && gcloud auth activate-service-account --key-file=${GOOGLE_SERVICE_ACCOUNT_FILE}
#RUN gsutil cp gs://elexis_mwsa_models/en.pkl /usr/src/app/models/en.pkl

RUN apt install -y python3-pip
RUN apt install -y git
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir --default-timeout=100 -r requirements.txt
RUN python3 -m nltk.downloader wordnet

COPY . /usr/src/app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["-m", "swagger_server"]