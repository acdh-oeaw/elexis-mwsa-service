import unittest
from unittest.mock import Mock

from swagger_server.models import DefinitionPair, ScoreInput
from swagger_server.services.service import AlignmentScoringService


class TestDefaultController(unittest.TestCase):

    def test_scoring(self):
        self.english_model_service = Mock()
        self.english_model_service.predict.return_value = zip(['broader', 'narrower', 'exact', 'none','related'],
                                                              [0.0, 0.0, 1.0, 0.0, 0.0])
        pair = DefinitionPair('test word', 'noun', 'en', 'Test def 1', 'Test def 1')
        score_input = ScoreInput('randomforest', pair)
        alignment_service = AlignmentScoringService(english_model=self.english_model_service)
        result = alignment_service.score(score_input)
        print(result)
        self.assertIsNotNone(result)
        #self.assertIsNotNone(result.alignment)
        #self.assertIsNotNone(result.probability)