# coding: utf-8

from __future__ import absolute_import

import pytest
from flask import json

from swagger_server.models.definition_pair import DefinitionPair  # noqa: E501
from swagger_server.models.score_input import ScoreInput
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""
    @pytest.mark.skip(reason="not available yet")
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

    def test_acdha_mwsa_scores_not_supported_languages(self):
        body = ScoreInput('bert', DefinitionPair(headword='test', pos='noun', lang='xx', def1='TEST_1', def2='TEST_2'))
        response = self.client.open(
            '/ACDH/ACDH_MWSA_Service/1o/achda-mwsa/scores/',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert400(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        self.assertIn('Language {} not supported'.format('xx'), response.json['detail'])

    def test_acdh_mwsa_get(self):
        """Test case for acdh_mwsa_get

        readiness check
        """
        response = self.client.open(
            '/ACDH/ACDH_MWSA_Service/1o/acdh-mwsa',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
