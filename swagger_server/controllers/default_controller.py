import connexion
import six

from swagger_server.exceptions.exceptions import LanguageNotSupportedException, NotSupportedLanguageProblem
from swagger_server.models.definition_pair import DefinitionPair  # noqa: E501
from swagger_server.models.features import Features  # noqa: E501
from swagger_server.models.score_input import ScoreInput
from swagger_server.models.scores import Scores  # noqa: E501
from swagger_server import util
from swagger_server.services.service import AlignmentScoringService


def acdh_mwsa_features_post(body=None):  # noqa: E501
    """Extract features for given definition pair

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: List[Features]
    """
    if connexion.request.is_json:
        body = DefinitionPair.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def achda_mwsa_scores_post(alignment_scoring_service: AlignmentScoringService, body=None):  # noqa: E501
    """Get word sense alignment of definition pairs

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: List[Scores]
    """
    results = []
    if connexion.request.is_json:
        score_input = ScoreInput.from_dict(body)  # noqa: E501
        try:
            results.extend(alignment_scoring_service.score(score_input))
        except LanguageNotSupportedException as lnse:
            raise NotSupportedLanguageProblem(status=400, title="Language not supported", detail=str(lnse))
        print(results)
    return results


def acdh_mwsa_get():  # noqa: E501
    """readiness check

     # noqa: E501


    :rtype: None
    """
    return 'do some magic!'
