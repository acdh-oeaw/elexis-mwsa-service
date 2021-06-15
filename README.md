# Swagger generated server

## Overview
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.  This
is an example of building a swagger-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m swagger_server
```

and open your browser to here:

```
http://localhost:8080/ACDH/ACDH_MWSA_Service/1o/ui/
```

Your Swagger definition lives here:

```
http://localhost:8080/ACDH/ACDH_MWSA_Service/1o/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 5000:5000 swagger_server
docker run -p 5000:5000 -v {model_path_host:/mwsa} --env MODEL_PATH=/mwsa {image id} 
```


#pip install -e git+ssh://gitlab+deploy-token-218175:5yjZ4VbaUkDExr5fag-X@gitlab.com/acdh-oeaw/elexis/mwsa_model.git#egg=mwsa_model

## Example Query
```
curl --location --request POST 'http://localhost:8080/ACDH/ACDH_MWSA_Service/1o/achda-mwsa/scores/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "classifier": "bert",
  "pair": {
    "headword":"olive",
    "pos":"noun",
    "lang": "de",
    "def1": "a type of edible fruit",
    "def2": "a type of edible fruit which is used as a garnish etc and which gives oil used for cooking"
  }
}'

curl --location --request POST 'https://mwsa-service.acdh-dev.oeaw.ac.at/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "classifier": "randomforst",
  "pair": {
    "headword": "olive",
    "pos": "noun",
    "lang": "en",
    "def1": "a type of edible fruit",
    "def2": "a type of edible fruit which is used as a garnish etc and which gives oil used for cooking"
  }
}'
```
