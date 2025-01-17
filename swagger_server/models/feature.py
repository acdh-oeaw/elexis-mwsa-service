# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Feature(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, value: float=None):  # noqa: E501
        """Feature - a model defined in Swagger

        :param name: The name of this Feature.  # noqa: E501
        :type name: str
        :param value: The value of this Feature.  # noqa: E501
        :type value: float
        """
        self.swagger_types = {
            'name': str,
            'value': float
        }

        self.attribute_map = {
            'name': 'name',
            'value': 'value'
        }
        self._name = name
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Feature':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Feature of this Feature.  # noqa: E501
        :rtype: Feature
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Feature.

        name of the feature  # noqa: E501

        :return: The name of this Feature.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Feature.

        name of the feature  # noqa: E501

        :param name: The name of this Feature.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def value(self) -> float:
        """Gets the value of this Feature.

        value of the feature  # noqa: E501

        :return: The value of this Feature.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value: float):
        """Sets the value of this Feature.

        value of the feature  # noqa: E501

        :param value: The value of this Feature.
        :type value: float
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value
