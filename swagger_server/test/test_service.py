from unittest.mock import Mock
import pandas as pd
import pytest

from swagger_server.models import DefinitionPair, ScoreInput
from swagger_server.services.service import AlignmentScoringService, ModelService

testdata = [
    DefinitionPair("Test Word", 'noun', 'en', 'English Definition 1', 'English Definition 2'),
    DefinitionPair("Test Wort", 'noun', 'de', 'German Definition 1', 'German Definition 2')
]


@pytest.mark.parametrize("pair", testdata)
def test_scoring(pair):
    model_service = Mock()
    model_service.predict.return_value = zip(['broader', 'narrower', 'exact', 'none', 'related'],
                                             [0.0, 0.0, 1.0, 0.0, 0.0])
    score_input = ScoreInput('randomforest', pair)
    alignment_service = AlignmentScoringService(lang_model=model_service)
    result = alignment_service.score(score_input)
    print(result)
    assert result is not None
    assert len(result) > 0


english_data = pd.DataFrame(
    data={'word': ['Test Word'], 'pos': ['noun'], 'def1': ['English Definition 1'],
          'def2': ['English Definition 2']})

german_data = pd.DataFrame(
    data={'word': ['Test Wort'], 'pos': ['noun'], 'def1': ['German Definition 1'],
          'def2': ['German Definition 2']})

testdata_2 = [
    ('en', english_data),
    ('de', german_data)
]


@pytest.mark.parametrize("lang, pair", testdata_2)
def test_prediction(lang, pair):
    mwsa_model_service = ModelService()
    result = mwsa_model_service.predict(lang, pair)

    assert result is not None
