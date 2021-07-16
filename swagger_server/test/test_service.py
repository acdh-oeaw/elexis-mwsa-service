from unittest.mock import Mock
import pandas as pd
import pytest

from swagger_server.exceptions.exceptions import LanguageNotSupportedException
from swagger_server.models import DefinitionPair, ScoreInput
from swagger_server.services.service import AlignmentScoringService, ModelService, TransformerService

testdata = [
    DefinitionPair("Test Word", 'noun', 'en', 'English Definition 1', 'English Definition 2'),
    DefinitionPair("Test Wort", 'noun', 'de', 'German Definition 1', 'German Definition 2'),
    DefinitionPair("Test Wort", 'de', 'German Definition 1', 'German Definition 2'),
    DefinitionPair("Test Wort", 'noun', 'xx', 'German Definition 1')
]

test_wrong_data = [
    DefinitionPair("Test Wort", 'de', 'German Definition 1', 'German Definition 2'),
    DefinitionPair("Test Wort", 'noun', 'xx', 'German Definition 1')
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
    assert len(result) == 5


@pytest.mark.parametrize("pair", testdata)
def test_scoring_with_bert(pair):
    transformer_service = Mock()
    transformer_service.predict.return_value = zip(['broader', 'narrower', 'exact', 'none', 'related'],
                                                   [0.0, 0.0, 1.0, 0.0, 0.0])
    score_input = ScoreInput('bert', pair)
    alignment_service = AlignmentScoringService(transformer_model=transformer_service)
    result = alignment_service.score(score_input)
    print(result)
    assert result is not None
    assert len(result) == 5


english_data = pd.DataFrame(
    data={'word': ['Test Word'], 'pos': ['noun'], 'def1': ['English Definition 1'],
          'def2': ['English Definition 2']})

german_data = pd.DataFrame(
    data={'word': ['Test Wort'], 'pos': ['noun'], 'def1': ['German Definition 1'],
          'def2': ['German Definition 2']})

testdata_2 = [
    ('en', english_data) # ,
   # ('de', german_data)
]


def test_not_supported_language():
    mwsa_model_service = ModelService()
    with pytest.raises(LanguageNotSupportedException):
        result = mwsa_model_service.predict('xx', english_data)


def test_not_supported_language_bert():
    mwsa_model_service = TransformerService()
    with pytest.raises(LanguageNotSupportedException):
        result = mwsa_model_service.predict('xx', english_data)

@pytest.mark.parametrize("lang, pair", testdata_2)
def test_prediction(lang, pair):
    mwsa_model_service = ModelService()
    result = mwsa_model_service.predict(lang, pair)

    assert result is not None

@pytest.mark.parametrize("lang, pair", testdata_2)
def test_prediction_with_bert(lang, pair):
    mwsa_model_service = TransformerService()
    result = mwsa_model_service.predict(lang, pair)

    assert result is not None
