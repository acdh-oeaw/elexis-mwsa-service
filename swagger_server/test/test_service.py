import pickle
import unittest

from swagger_server.models import DefinitionPair, ScoreInput
from swagger_server.services.service import AlignmentScoringService


class TestDefaultController(unittest.TestCase):

    def test_extract_features(self):
        pair = DefinitionPair('test word', 'noun', 'en', 'Test def 1', 'Test def 1')
        score_input = ScoreInput('randomforest', pair)
        alignment_service = AlignmentScoringService()
        result = alignment_service.score(score_input)
        print(result)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.alignment)
        self.assertIsNotNone(result.probability)
