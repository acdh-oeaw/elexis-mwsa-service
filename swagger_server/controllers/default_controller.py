import connexion
import six

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.definition_pair import DefinitionPair  # noqa: E501
from swagger_server.models.features import Features  # noqa: E501
from swagger_server.models.scores import Scores  # noqa: E501
from swagger_server import util


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


def achda_mwsa_scores_post(body=None):  # noqa: E501
    """Get word sense alignment of definition pairs

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: List[Scores]
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
