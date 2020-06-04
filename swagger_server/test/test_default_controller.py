# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.definition_pair import DefinitionPair  # noqa: E501
from swagger_server.models.features import Features  # noqa: E501
from swagger_server.models.score_input import ScoreInput
from swagger_server.models.scores import Scores  # noqa: E501
from swagger_server.services.service import FeatureExtractionService
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_acdh_mwsa_features_post(self):
        """Test case for acdh_mwsa_features_post

        Extract features for given definition pair
        """
        body = DefinitionPair()
        response = self.client.open(
            '/ACDH/ACDH_MWSA_Service/1o/acdh-mwsa/features',
            method='POST',
            data=json.dumps(body),
            content_type='applciation/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_achda_mwsa_scores_post(self):
        """Test case for achda_mwsa_scores_post

        Get word sense alignment of definition pairs
        """
        body = ScoreInput('bert', DefinitionPair(headword='test', pos='noun', lang='de', def1='TEST_1', def2='TEST_2'))
        response = self.client.open(
            '/ACDH/ACDH_MWSA_Service/1o/achda-mwsa/scores/',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn('alignment', response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
