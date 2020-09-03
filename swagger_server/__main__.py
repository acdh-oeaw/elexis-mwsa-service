#!/usr/bin/env python3

import connexion
import logging
from swagger_server import encoder
from injector import Binder
from flask_injector import FlaskInjector
from swagger_server.services.service import AlignmentScoringService

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def configure(binder:Binder):
    binder.bind(
        AlignmentScoringService,
        AlignmentScoringService()
    )

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'ACDH MWSA Service'}, pythonic_params=True)
    FlaskInjector(app=app.app, modules=[configure])
    app.run(port=5000)


if __name__ == '__main__':
    main()
