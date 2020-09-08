import logging

import connexion
from flask_testing import TestCase
from injector import Binder
from flask_injector import FlaskInjector

from swagger_server.encoder import JSONEncoder
from swagger_server.services.service import AlignmentScoringService


def configure(binder: Binder):
    binder.bind(
        AlignmentScoringService,
        AlignmentScoringService()
    )


class BaseTestCase(TestCase):

    def create_app(self):
        logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        app.app.json_encoder = JSONEncoder
        app.add_api('swagger.yaml')
        FlaskInjector(app=app.app, modules=[configure])
        return app.app
