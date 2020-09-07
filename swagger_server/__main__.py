#!/usr/bin/env python3

import connexion
import logging

import flask

from swagger_server import encoder
from injector import Binder
from flask_injector import FlaskInjector
from swagger_server.services.service import AlignmentScoringService

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = connexion.App(__name__, specification_dir='./swagger/')

@app.app.before_request
def before_request_func():
    logger.debug(flask.current_app.url_map)

def configure(binder: Binder):
    binder.bind(
        AlignmentScoringService,
        AlignmentScoringService()
    )


def main():
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'ACDH MWSA Service'}, pythonic_params=True)
    FlaskInjector(app=app.app, modules=[configure])
    app.run(port=5000, debug=True)


if __name__ == '__main__':
    main()
